# this module used to get inputs like height and weight to GUI

import json
from flask import request
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
import Global_var
from ttkthemes import ThemedTk
from Helper_module import get_inputs, reset_inputs, send_request, validate_all_fields, validate_range,transete
import GUI_Template
import re
import time
import threading as th
import serial as ser
import numpy as NP

class weightHeight:

    labelFont = None
    addressFont = None
    next_frame = None
    weights = []
    heights = []
    device_connected = True
    weight_text = None
    height_text = None
    submit_button = None
    restart_test = None
    weight_median = 0
    height_median = 0
    def __init__(self, main):
        self.main = main
        self.labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        self.addressFont = tkFont.Font(family="Andalus", size=20, weight="bold")
    
    def reset(self):
        self.weights = []
        self.heights = []
    
    def window(self):
        self.main.title("الطول و الوزن")   
        self.main.geometry("600x300")
        self.main.minsize(600,300)
        self.main.maxsize(600,300)
        try:
            self.se = ser.Serial(f'COM{Global_var.COMport}', 9600, timeout=1)
        except Exception:
            self.device_connected = False
        adress_label = ttk.Label(self.main, text="تسجيل الطول و الوزن",font = self.addressFont)
        id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont).place(x = 300,y = 50)
        name_label = ttk.Label(self.main, text=":الاسم",font = self.labelFont).place(x = 457,y = 75)
        name_content_l = ttk.Label(self.main, text=f"{Global_var.name}", font=self.labelFont).place(x=300, y=75)
        height_label = (ttk.Label(self.main, text="الطول",font = self.labelFont)).place(x=450, y= 150)
        self.height_text = ttk.Entry(self.main,width=8)
        self.height_text.place(x = 380,y = 150)
        weight_label = (ttk.Label(self.main, text="الوزن",font = self.labelFont)).place(x=280, y= 150)
        self.weight_text = ttk.Entry(self.main,width=8)
        self.weight_text.place(x = 210,y = 150)
        hUint_label = ttk.Label(self.main, text= "سم", font= self.labelFont).place(x=360, y=150)
        wUint_label = ttk.Label(self.main, text= "كجم", font= self.labelFont).place(x=185, y=150)
        self.submit_button = ttk.Button(self.main,text="حفظ",width=10, command=self.submit)
        self.submit_button.place(x= 340,y = 200)
        self.restart_test = ttk.Button(self.main,text="اعادة القياس",width=10, command=self.start_thread)
        self.restart_test.place(x= 220,y = 200)
        self.start_thread()
    
    def start_thread(self):
        if self.device_connected:
            t1=th.Thread(target=self.start_lestining)
            self.stop_thread = False
            t1.daemon = True
            t1.start()
                
    def validations(self,data):
        msg = ""
        Flag = True
        if not validate_all_fields(data):
            msg = "يجب ملئ كل الخانات"
            Flag = False
        elif not validate_range(data[0],60,250):
            Flag = False
            msg = 'الطول خاطئ'
        elif not validate_range(data[1],30,200):
            Flag = False
            msg = 'الوزن خاطئ'
        if not Flag:    
            messagebox.showerror("خطأ",msg)
        return Flag,msg
    
    def start_lestining(self):
        self.submit_button['state'] = tk.DISABLED
        self.restart_test['state'] = tk.DISABLED
        start = int(time.time())
        time.sleep(5)
        
        while int(time.time()) - start < 5:
            s = self.se.readline()
            s = s.decode('UTF-8')
            d = s.split(":")
            if d[0] == "Weight":
                d[1] = d[1].strip()
                self.weights.append(round(float(d[1]),2))
            elif d[0] == "Length":
                d[1] = d[1].strip()
                self.heights.append(round(float(d[1]),1))
        self.calculate_median()
        self.change_text()
        self.submit_button['state'] = tk.NORMAL
        self.restart_test['state'] = tk.NORMAL
    
    def calculate_median(self):
        self.weight = NP.median(self.weights)
        self.height = NP.median(self.heights)
    
    def change_text(self):
        if self.weight_median != 0:
            self.weight_text.delete(0,"end")
            self.weight_text.insert(0,"{:.2f}".format(self.weight_median))
        if self.height_median != 0:
            self.height_text.delete(0,"end")
            self.height_text.insert(0,"{:.2f}".format(self.height_median))            
    
    def formulate_data(self,id,name,height,weight):
        data = {
                "id":int(id),
                "name":name,
                "height":int(height),
                "weight":int(weight)
            }
        return data
                
    def submit(self):
        data = get_inputs(self.main)
        flag,msg = self.validations(data)
        if flag:
            data = self.formulate_data(Global_var.mil_id,Global_var.name,data[0],data[1])
            send_request(data,Global_var.ip,"weightHeight")
            self.next_frame = GUI_Template.InforamtionPage(self.main,self)
            transete(self.main,self.next_frame)
            reset_inputs(self.main)
            
root = ThemedTk(theme="breeze")
wh = weightHeight(root)
master = GUI_Template.InforamtionPage(root,wh,True)
master.window()
root.mainloop()  