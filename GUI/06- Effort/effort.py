# this module used to get inputs like height and weight to GUI
import json
from flask import request
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
import Global_var
from ttkthemes import ThemedTk
from Helper_module import get_inputs, send_request, transete, validate_all_fields, validate_range
import GUI_Template
######################################GUI#########################################    
class effort:
    labelFont = None
    addressFont = None
    next_frame = None
    def __init__(self,main):
        self.main = main
    def window(self):
        self.main.geometry("600x300")
        self.main.minsize(600,300)
        self.main.maxsize(600,300)
        self.labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        self.addressFont = tkFont.Font(family="Andalus", size=20, weight="bold")  
        self.main.title("عجلة بذل الجهد")
        adress_label = ttk.Label(self.main, text="عجلة بذل الجهد",font = self.addressFont)
        id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont).place(x = 300,y = 50)
        name_label = ttk.Label(self.main, text=":الاسم",font = self.labelFont).place(x = 457,y = 75)
        name_content_l = ttk.Label(self.main, text=f"{Global_var.name}", font=self.labelFont).place(x=300, y=75)        
        heart_label = (ttk.Label(self.main, text="دقات القلب",font = self.labelFont)).place(x=415, y= 150)
        heart_text = ttk.Entry(self.main,width=10)
        heart_text.place(x = 320,y = 150)
        submit_button = ttk.Button(self.main,text="حفظ",width=10, command=self.submit).place(x= 280,y = 200)
##################################################################################

    def validations(self,data):
        msg = ""
        Flag = True
        if not validate_all_fields(data):
            msg = "يجب ملئ كل الخانات"
            Flag = False
        elif not validate_range(data[0],10,200):
            Flag = False
            msg = 'دقات قلب خاطئة'
        if not Flag:    
            messagebox.showerror("خطأ",msg)
        return Flag        

    def formulate_data(self,data):
        data = {
            "id":Global_var.mil_id,
            "name":Global_var.name,
            "effortMarkData":int(data[0]),
        }
        return data
        
    def submit(self):
        data = get_inputs(self.main)
        flag = self.validations(data)
        if flag:
            data = self.formulate_data(data)
            send_request(data,Global_var.ip,"effortMeasure")
            self.next_frame = GUI_Template.InforamtionPage(self.main,self)
            transete(self.main,self.next_frame)
root = ThemedTk(theme="breeze")
wh = effort(root)
master = GUI_Template.InforamtionPage(root,wh)
master.window()
root.mainloop()  