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

class weightHeight:

    labelFont = None
    addressFont = None
    next_frame = None
    def __init__(self, main):
        self.main = main
        self.labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        self.addressFont = tkFont.Font(family="Andalus", size=20, weight="bold")
    def window(self):
        self.main.title("الطول و الوزن")   
        self.main.geometry("600x300")
        self.main.minsize(600,300)
        self.main.maxsize(600,300)
        adress_label = ttk.Label(self.main, text="تسجيل الطول و الوزن",font = self.addressFont)
        id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont).place(x = 300,y = 50)
        name_label = ttk.Label(self.main, text=":الاسم",font = self.labelFont).place(x = 457,y = 75)
        name_content_l = ttk.Label(self.main, text=f"{Global_var.name}", font=self.labelFont).place(x=300, y=75)
        height_label = (ttk.Label(self.main, text="الطول",font = self.labelFont)).place(x=450, y= 150)
        height_text = ttk.Entry(self.main,width=8)
        height_text.place(x = 380,y = 150)
        weight_label = (ttk.Label(self.main, text="الوزن",font = self.labelFont)).place(x=280, y= 150)
        weight_text = ttk.Entry(self.main,width=8)
        weight_text.place(x = 210,y = 150)
        hUint_label = ttk.Label(self.main, text= "سم", font= self.labelFont).place(x=360, y=150)
        wUint_label = ttk.Label(self.main, text= "كجم", font= self.labelFont).place(x=185, y=150)
        submit_button = ttk.Button(self.main,text="حفظ",width=10, command=self.submit).place(x= 280,y = 200)
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
master = GUI_Template.InforamtionPage(root,wh)
master.window()
root.mainloop()  