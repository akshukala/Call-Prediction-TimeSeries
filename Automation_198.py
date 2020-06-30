# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:54:51 2020

@author: akshay.kale
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
import datetime
import itertools
from openpyxl import load_workbook
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

warnings.filterwarnings("ignore")

def test_stationarity(timeseries):
    
    '''Determing rolling statistics'''
    rolmean = timeseries.rolling(window=12).mean()
    rolstd = timeseries.rolling(window=12).std()
    '''Plot rolling statistics:'''
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)    
    '''Perform Dickey-Fuller test:'''
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)
    return dfoutput

def predictions_ARIMA(data, call_type, type_ts):
    '''
        call_type = (Offered Calls, AT)
        type_ts = (ARIMA, SARIMA)
    '''
    data.Date = pd.to_datetime(data.Date)
    data.set_index('Date', inplace=True)
    ts = data[call_type]
    stationarity = test_stationarity(ts)

    ts_log = np.log(ts)
    ts_lag_diff = ts_log - ts_log.shift()
    ts_lag_diff.dropna(inplace=True)
    stationarity = test_stationarity(ts_lag_diff)
    '''ARIMA model'''
    model = ARIMA(ts_log, order=(1, 1, 0))  
    results_ARIMA = model.fit(disp=-1)
    predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
    '''Converting predicted values to its orihinal form'''
    predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
    predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
    predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    predictions = np.exp(predictions_ARIMA_log)
    df = predictions.to_frame()
    previous_date = predictions.index[-1]
    df['Date1'] = df.index
    df.reset_index(inplace = True, drop = True)
    df.columns = [type_ts, 'Date']
    df.dropna(inplace=True)
    '''Predicting values for next 7 days'''
    next_seven_days = results_ARIMA.forecast(steps=7)
    next_seven_days = np.exp(next_seven_days[0])
    next_pred = pd.DataFrame(next_seven_days)
    next_pred['date'] = pd.date_range(start=previous_date + datetime.timedelta(days=1), periods=7, freq='D')
    next_pred.columns = [type_ts, 'Date']
    df = pd.concat([df, next_pred], axis=0)
    return df    

def predictions_SARIMA(data, call_type, type_ts):
    ts = data[call_type]
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    AIC = []
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(ts,
                                                order=param,
                                                seasonal_order=param_seasonal,
                                                enforce_stationarity=False,
                                                enforce_invertibility=False)
                results = mod.fit()
                temp = {}
                temp[str(param) + "X" + str(param_seasonal) ] = results.aic
                AIC.append(temp)
               # print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
            except:
                continue
    '''Getting pdq values for applying seasonal ARIMA'''
    pdq = sorted(AIC, key=lambda x: list(x.values()))[0]
    pdq = list(pdq.keys())[0].split('X')
    param1_tuple = pdq[0].replace('(', '')
    param1_tuple = param1_tuple.replace(')', '')
    param1 = tuple(map(int, param1_tuple.split(',')))

    param2_tuple = pdq[1].replace('(', '')
    param2_tuple = param2_tuple.replace(')', '')
    param2 = tuple(map(int, param2_tuple.split(',')))
    
    mod = sm.tsa.statespace.SARIMAX(ts,
                                order=param1,
                                seasonal_order=param2,
                                enforce_stationarity=False,
                                enforce_invertibility=False)
    results = mod.fit()
    
    pred = results.get_prediction()
    y_forecasted = pred.predicted_mean
    y_truth = ts['01-04-2019':]
    mse = ((y_forecasted - y_truth) ** 2).mean()    
    pred_uc = results.get_forecast(steps=7)
    pred_ci = pred_uc.predicted_mean
    df = pd.concat([y_forecasted, pred_ci], axis=0).to_frame()
    df['Date1'] = df.index
    df.reset_index(inplace = True, drop = True)
    df.columns = [type_ts, 'Date']
    return df
    
def create_result_sheet(result, start_col, type_ts, sheet_name, path):
    '''Writing predicted result to the existing excel sheet.'''
    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book
    writer.sheets = {ws.title: ws for ws in book.worksheets}
    result[type_ts].to_excel(writer,sheet_name=sheet_name, startcol=start_col, index=False)
    writer.save()

def error_percentage(sheet_name, call_type, path):
    '''Calculate percentage eror betwwen actual and predicted values.'''
    temp_df = pd.DataFrame()    
    data = pd.read_excel(path, sheet_name=sheet_name)
    temp_df['ARIMA % Error'] = round(((pd.to_numeric(data['ARIMA']) - pd.to_numeric(data[call_type])
                                        )/pd.to_numeric(data[call_type]))*100, 2)
    temp_df['SARIMA % Error'] = round(((pd.to_numeric(data['SARIMA']) - pd.to_numeric(data[call_type])
                                        )/pd.to_numeric(data[call_type]))*100, 2)
    create_result_sheet(temp_df, 4, ['ARIMA % Error','SARIMA % Error'], sheet_name, path)
    return "Success"

def main_func(sheet_name, call_type, path):
    '''Reading input file'''
    data = pd.read_excel(path, sheet_name=sheet_name)
    '''Appling ARIMA on data'''
    arima_result = predictions_ARIMA(data, call_type, 'ARIMA')
    '''Updating the predictions in sheet.'''
    create_result_sheet(arima_result, 2, 'ARIMA', sheet_name, path)
    '''Applying SARIMA on data'''
    sarima_result = predictions_SARIMA(data, call_type, 'SARIMA')
    create_result_sheet(sarima_result, 3, 'SARIMA', sheet_name, path)
    
    percentage_error = error_percentage(sheet_name, call_type, path)
    return "Successfully predicted " + str(path)
