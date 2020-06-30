# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:54:51 2020

@author: akshay.kale
"""

import tkinter as tk
from tkinter.ttk import Style
from tkinter import messagebox
from tkinter import filedialog
from Automation_198 import main_func

'''Create a tkinter object.'''
root = tk.Tk()
'''Create a style object.'''
s = Style()
s.theme_use('xpnative')
root.title("Time Series")
root.geometry('650x450')
root.resizable(False, False) 
'''Creating heading label'''
lbl1 = tk.Label(root, text="Time Series Analysis",
                fg = "#C70039", font = "Calibri 22 bold")
lbl1.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

lbl2 = tk.Label(root, text="Predict Calls for 198 Helpline: ",
                fg = "black", anchor="w", font = "Calibri 12")
lbl2.place(relx=0.03, rely=0.2)
'''Browse file button'''
def browse_button_198():
    filename = filedialog.askopenfilename()
    file_path_198.set(filename)

file_path_198 = tk.StringVar()
lbl6 = tk.Label(root, text="198 Data File Path: ", fg = "black", anchor="w", font="Calibri 12")
entry_198 = tk.Entry(root, width=45, textvariable=file_path_198)
browsebutton1 = tk.Button(root, text="Browse", command = browse_button_198)
lbl6.place(relx=0.13, rely=0.15, anchor=tk.CENTER)
entry_198.place(relx=0.5, rely=0.15, anchor=tk.CENTER)
browsebutton1.place(relx=0.83, rely=0.15, anchor=tk.CENTER)

'''198 prediction function call.'''
def helpline_198():
    path_198 = entry_198.get()
    res_offered = main_func('198_prepaid_offered', 'OfferedCalls', path_198)
    res_at = main_func('198_prepaid_AT', 'AT', path_198)
    print(res_at)
    print(res_offered)
    res_offered_post = main_func('198_postpaid_offered', 'OfferedCalls', path_198)
    res_at_post = main_func('198_postpaid_AT', 'AT', path_198)
    messagebox.showinfo("Information","Successfully completed the predictions.")

btn = tk.Button(root, text="Predict Calls", command = helpline_198)
btn.place(relx=0.45, rely=0.23, anchor=tk.CENTER)

lbl3 = tk.Label(root, text="------------------------------------------------------------------------",
                fg = "#7E7477", font = "Calibri 22 bold")
lbl3.place(relx=0.5, rely=0.35, anchor=tk.CENTER)



def browse_button_12345():
    filename = filedialog.askopenfilename()
    file_path_12345.set(filename)

file_path_12345 = tk.StringVar()
lbl4 = tk.Label(root, text="12345 Data File Path: ", fg = "black", anchor="w", font="Calibri 12")
entry_12345 = tk.Entry(root, width=45, textvariable=file_path_12345)
browsebutton2 = tk.Button(root, text="Browse", command = browse_button_12345)
lbl4.place(relx=0.14, rely=0.45, anchor=tk.CENTER)
entry_12345.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
browsebutton2.place(relx=0.83, rely=0.45, anchor=tk.CENTER)


lbl5 = tk.Label(root, text="Predict Calls for 12345 Helpline: ",
                fg = "black", anchor="w", font = "Calibri 12")
lbl5.place(relx=0.03, rely=0.55)


'''12345 prediction function call'''
def helpline_12345():
    path_12345 = entry_12345.get()
    res_offered = main_func('12345_prepaid_offered', 'OfferedCalls', path_12345)
    res_at = main_func('12345_prepaid_AT', 'AT', path_12345)
    print(res_at)
    print(res_offered)
    res_offered_post = main_func('12345_postpaid_offered', 'OfferedCalls', path_12345)
    res_at_post = main_func('12345_postpaid_AT', 'AT', path_12345)
    messagebox.showinfo("Information","Successfully completed the predictions.")

btn1 = tk.Button(root, text="Predict Calls", command = helpline_12345)
btn1.place(relx=0.45, rely=0.58, anchor=tk.CENTER)


root.mainloop()