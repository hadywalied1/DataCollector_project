
import time
from flask import request
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
import Global_var
from ttkthemes import ThemedTk
from Helper_module import clear_window, get_inputs, send_request, transete, validate_all_fields, validate_range
import GUI_Template
import serial as ser
import re
import threading as th

class handStability:
    test_counter = 0
    test_counters = [0,0,0,0]
    test_times = [0,0,0,0]
    test_averages = [0,0,0,0]
    tot_err_avg = tot_time_avg = 0
    stop_thread = False
    labelFont = None
    addressFont = None
    se = None
    tests = ["التجريبي","الاول","الثاني","الثالث"]
    error_text = None
    error_time_text = None
    next_frame = None
    device_connected = True
    def __init__(self,main):
        self.main = main
        
######################################GUI#########################################        
    def window(self):
        self.main.title("ثبات الذراعين")
        self.main.geometry("600x300")
        self.labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        self.addressFont = tkFont.Font(family="Andalus", size=20, weight="bold")
        self.main.minsize(600,300)
        self.main.maxsize(600,300) 
        try:
            self.se = ser.Serial(f'COM{Global_var.COMport}', 9600, timeout=1)
            self.test_window()
        except Exception:
            self.device_connected = False
            messagebox.showerror("خطأ","البرنامج لا يرى جهاز الأردوينو تأكد من ان الجهاز متصل او ان رقم البورت صحيح")
            self.next_frame = GUI_Template.InforamtionPage(self.main,self,True)
            transete(self.main,self.next_frame)
            self.reset() 
        
    def reset(self):
        self.test_counter = 0
        self.test_counters = [0,0,0,0]
        self.test_times = [0,0,0,0]
        self.test_averages = [0,0,0,0]
        self.tot_err_avg = tot_time_avg = 0
        self.stop_thread = False
        self.labelFont = None
        self.addressFont = None
        self.se = None
        self.tests = ["التجريبي","الاول","الثاني","الثالث"]
        self.error_text = None
        self.error_time_text = None
        self.next_frame = None
        self.device_connected = True

    def submit(self,grade):
        data = self.formulate_data(grade)
        send_request(data,Global_var.ip,"handStability")
        time.sleep(0.5)
        self.next_frame = GUI_Template.InforamtionPage(self.main,self,True)
        transete(self.main,self.next_frame)
        self.reset()

    def calculate_average(self):
        for i in range(1,4):
            self.tot_err_avg+=self.test_counters[i]
        for i in range(1,4):
            self.tot_time_avg+=self.test_averages[i]
        self.tot_err_avg//=3
        self.tot_time_avg/=3

    def calculate_grade(self,num,avg_time):
        if num <= 27:
            if avg_time < 3.57:
                return 1
            else:
                return 2
        else:
            if avg_time < 3.57:
                return 3
            else:
                return 4
        
    def grade_btn_action(self):
        global stop_thread
        if len(self.error_text.get()) == 0 or len(self.error_time_text.get()) == 0:
            messagebox.showerror("خطأ","يجب ملئ كل الخانات")
        else:
            stop_thread = True
            clear_window(self.main)
            self.calculate_average()
            gradee = self.calculate_grade(self.tot_err_avg,self.tot_time_avg)
            self.grade_window(gradee)

    def grade_window(self,grade):
            id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont).place(x = 260,y = 50)
            name_label = ttk.Label(self.main, text=":الاسم",font = self.labelFont).place(x = 484,y = 75)
            name_content_l = ttk.Label(self.main, text=f"{Global_var.name}", font=self.labelFont).place(x=300, y=75)
            label1 = ttk.Label(self.main, text=":متوسط عدد الاخطاء",font = self.labelFont).place(x=383, y= 100)
            num1 = ttk.Label(self.main, text=self.tot_err_avg,font = self.labelFont).place(x=340, y= 100)                      
            label2 = ttk.Label(self.main, text=":متوسط زمن الاخطاء",font = self.labelFont).place(x=380, y= 125)
            num2 = ttk.Label(self.main, text="{:.2f}".format(self.tot_time_avg),font = self.labelFont).place(x=340, y= 125)
            label3 = ttk.Label(self.main, text="النتيجة",font = self.addressFont).place(x=430, y= 150)
            num3 = ttk.Label(self.main, text=grade,font = self.addressFont).place(x=390, y= 150)
            restart_test_btn =  ttk.Button(self.main,text="حفظ",width=10, command=lambda: self.submit(grade)).place(x= 280,y = 200)  
            
    def exit_btn(self):
        if len(self.error_text.get()) == 0 or len(self.error_time_text.get()) == 0:
            messagebox.showerror("خطأ","يجب ملئ كل الخانات")
        else:
            self.stop_thread = True
            time.sleep(1)
            clear_window(self.main)
            self.test_window()
        
    def start_lestining(self,count,tm,average,idx):
        while True:
            if self.stop_thread:
                break
            s = self.se.readline()
            s = s.decode('UTF-8')
            n = re.findall(r'\d*\.\d+|\d+',s)
            if len(n) == 2:
                count[idx] +=1
                tm[idx] += float(n[1])
                if count[idx] != 0:
                    average[idx] = tm[idx]/count[idx]
                else:
                    average[idx] = 0
                if stop_thread:
                    break
                self.error_text.delete(0,"end")
                self.error_time_text.delete(0,"end")
                self.error_text.insert(0,count[idx])
                self.error_time_text.insert(0,"{:.2f}".format(average[idx]))

                               
    def test_window(self):
        self.error_text = ttk.Entry(self.main,width=5)
        self.error_text.place(x = 400,y = 125)
        self.error_time_text = ttk.Entry(self.main,width=5)
        self.error_time_text.place(x = 170,y = 125)
        '''if self.device_connected:
            t1=th.Thread(target=self.start_lestining,args=(self.test_counters,self.test_times,self.test_averages,self.test_counter))
            self.stop_thread = False
            t1.daemon = True
            t1.start()
        '''
        
        test_label = ttk.Label(self.main, text=f"الاختبار {self.tests[self.test_counter]}",font = self.addressFont)
        self.test_counter+=1
        id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont)
        id_label.place(x = 275,y = 50)
        name_label = ttk.Label(self.main, text=":الاسم",font = self.labelFont)
        name_label.place(x = 500,y = 85)
        name_content_l = ttk.Label(self.main, text=f"{Global_var.name}", font=self.labelFont)
        name_content_l.place(x=300, y=85)
        test_label.pack()                       
        error_num = (ttk.Label(self.main, text=":عدد الاخطاء",font = self.labelFont))
        error_num.place(x=460, y= 125)
        error_time_label = (tk.Label(self.main, text=":متوسط زمن الخطأ",font = self.labelFont))
        error_time_label.place(x=220, y=125)
        next_test_btn = ttk.Button(self.main,text="الاختبار التالي",width=10, command=self.exit_btn)
        grade_btn = ttk.Button(self.main,text="اظهار النتيجة",width=10,command= self.grade_btn_action)   
        if self.test_counter < 4:
            next_test_btn.place(x= 280,y =200)        
        else:       
            grade_btn.place(x= 280,y = 200)
        
    def formulate_data(self,grade):
        data = {
                "id":Global_var.mil_id,
                "name":Global_var.name,
                "firstWrongCount":int(self.test_counters[0]),
                "firstTotalTime":float(self.test_times[0]),
                "firstAvg": float(self.test_averages[0]), 
                "secondWrongCount":int(self.test_counters[1]),
                "secondTotalTime":float(self.test_times[1]),
                "secondAvg": float(self.test_averages[1]),
                "thirdWrongCount":int(self.test_counters[2]),
                "thirdTotalTime":float(self.test_times[2]),
                "thirdAvg": float(self.test_averages[2]),
                "handStabilityDegree": int(grade)
        }
        return data
        
root = ThemedTk(theme="breeze")
wh = handStability(root)
master = GUI_Template.InforamtionPage(root,wh,True)
master.window()
root.mainloop()  