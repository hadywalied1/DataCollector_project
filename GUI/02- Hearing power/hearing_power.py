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

class hearingPower:
    labelFont = None
    addressFont = None
    grades = ['غير لائق','مقبول','جيد','جيد جدا','امتياز']
    gradeL_num = None
    gradeR_num = None
    gR_label = None
    gL_label = None
    next_frame = None
######################################GUI#########################################
    def __init__(self,main):
        self.main = main
        self.labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        self.addressFont = tkFont.Font(family="Andalus", size=20, weight="bold")     
    def window(self):
        self.main.geometry("600x310")
        self.main.title("شدة السمع")
        self.main.minsize(600,300)
        self.main.maxsize(600,300)
        adress_label = ttk.Label(self.main, text="قياس شدة السمع",font = "arial 20 bold")
        id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont).place(x = 300,y = 50)
        name_label = ttk.Label(self.main, text=":الاسم",font = self.labelFont).place(x = 457,y = 75)
        name_content_l = ttk.Label(self.main, text=f"{Global_var.name}", font=self.labelFont).place(x=300, y=75)
        right_label = (ttk.Label(self.main, text="الاذن اليمنى",font = self.labelFont)).place(x=415, y= 150)
        right_text = ttk.Entry(self.main,width=8)
        right_text.place(x = 350,y = 150)
        left_label = (ttk.Label(self.main, text="الاذن اليسرى",font = self.labelFont)).place(x=240, y= 150)
        left_text = ttk.Entry(self.main,width=8)
        left_text.place(x = 180,y = 150)
        gradeR_label = (ttk.Label(self.main, text=":نتيجة اليمنى",font = self.labelFont)).place(x=415, y= 200)
        self.gR_label = (ttk.Label(self.main, text="",font = self.labelFont))
        self.gR_label.place(x=375, y= 200)
        gradeL_label = (ttk.Label(self.main, text=":نتيجة اليسرى",font = self.labelFont)).place(x=240, y= 200)
        self.gL_label = (ttk.Label(self.main, text="",font = self.labelFont))
        self.gL_label.place(x=200, y= 200)
        calculate_button = ttk.Button(self.main,text="حساب النتيجة",width=10, command=self.calculate_grade).place(x= 200,y = 250)
        submit_button = ttk.Button(self.main,text="حفظ",width=10, command=self.submit).place(x= 350,y = 250)
######################################GUI#########################################
    def validations(self,data):
        msg = ""
        Flag = True
        if not validate_all_fields(data):
            msg = "يجب ملئ كل الخانات"
            Flag = False
        elif not validate_range(data[0],0,2):
            Flag = False
            msg = 'نتيجة خاطئة'
        elif not validate_range(data[1],0,2):
            Flag = False
            msg = 'نتيجة خاطئة'
        if not Flag:    
            messagebox.showerror("خطأ",msg)
        return Flag

    def calculate_grade(self):
        global gradeL_num
        global gradeR_num
        data = get_inputs(self.main)
        flag = self.validations(data)
        if flag:
            gradeL_num = self.grades[int(data[0])]
            gradeR_num = self.grades[int(data[1])]
            self.gR_label.config(text = gradeR_num)
            self.gL_label.config(text = gradeL_num)
    
    def formulate_data(self,data):
        data = {
            "id":Global_var.mil_id,
            "name":Global_var.name,
            "rightEarDegree":data[0],
            "rightEarTones":self.grades[int(data[0])],
            "leftEarDegree":data[1],
            "leftEarTones":self.grades[int(data[1])]
        }
        return data       

    def submit(self):
        data = get_inputs(self.main)
        flag = self.validations(data)
        data = self.formulate_data(data)
        if flag:
            if gradeL_num is None or gradeR_num is None:
                messagebox.showerror('error', "قم بحساب النتيجة اولا")
            else:
                send_request(data,Global_var.ip,"hearing")
                self.next_frame = GUI_Template.InforamtionPage(self.main,self)
                transete(self.main,self.next_frame)

root = ThemedTk(theme="breeze")
wh = hearingPower(root)
master = GUI_Template.InforamtionPage(root,wh)
master.window()
root.mainloop()  

