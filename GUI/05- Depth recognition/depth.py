
import tkinter as tk
from tkinter import messagebox
from tkinter.messagebox import NO
import tkinter.ttk as ttk
import tkinter.font as tkFont
from ttkthemes import ThemedTk
from Helper_module import send_request, transete
from Helper_module import clear_window
import GUI_Template
import serial as ser
import time
import threading as th
import re
import Global_var
class DepthRecognintion:
    se = None 
    test_counter = [0]
    test_name = None
    test_list = ["المحاولة التجريبية","الاختبار الأول"]
    labelFont = None
    addressFont = None
    distance = None
    distance_text = None
    data_test = [0,0,0]
    data_trial = 0
    next_frame = None
    def __init__(self, main):
        self.main = main
        self.labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        self.addressFont = tkFont.Font(family="Andalus", size=20, weight="bold") 
        
    
    def window(self):
        self.main.title("اختبار ادراك العمق")   
        self.main.geometry("600x300")
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
        self.se = None 
        self.test_counter = [0]
        self.test_name = None
        self.test_list = ["المحاولة التجريبية","الاختبار الأول"]
        self.distance = None
        self.distance_text = None
        self.data_test = [0,0,0]
        self.data_trial = 0

    def test_window(self):
        adress_label = ttk.Label(self.main, text="اختبار ادراك العمق",font = self.addressFont)
        adress_label.place(x=200, y=15)
        adress_label_2 = ttk.Label(self.main, text=self.test_list[self.test_counter[0]],font = self.addressFont)
        adress_label_2.place(x=210, y=50)
        self.distance = (ttk.Label(self.main, text=":المسافة",font = self.labelFont))
        self.distance.place(x=430, y= 125)
        self.distance_text = ttk.Entry(self.main,width=10)
        self.distance_text.place(x = 335,y = 125)   
        if self.test_counter[0] < 1:
            self.next_btn()
        else:
            self.result_btn()  
        t1 = th.Thread(target=self.get_depth_data, args=(self.test_counter))
        t1.start()   
              
    def get_depth_data(self, test_count):
        while True:
            s = self.se.readline()
            s = s.decode('UTF-8')
            main_data = re.findall(r'\d*\.\d*',s)
            if len(main_data) != 0:
                self.distance_text.delete(0, "end")
                self.distance_text.insert(0, main_data[0])
                if test_count == 0:
                    self.data_trial = main_data[0]
                else:
                    self.data_test[0] = main_data[0]
                    self.data_test[1] = main_data[1]
                    self.data_test[2] = main_data[2]
                break
        
    def transition(self):
        if len(self.distance_text.get()) == 0:
            messagebox.showerror("خطأ","يجب ملئ كل الخانات")
        else:
            clear_window(self.main)
            self.test_counter[0]+=1
            self.test_window()
    

    def next_btn(self):
        next_test_btn = ttk.Button(self.main,text="الاختبار التالي",width=10, command=lambda:self.transition())            
        next_test_btn.place(x= 250,y = 200)        

    def result_btn(self):
        result_btn = ttk.Button(self.main,text="اظهار النتيجة",width=10, command=lambda:self.result_window())            
        result_btn.place(x= 250,y = 200)
        

    def result_window(self):
        clear_window(self.main)
        adress_label = ttk.Label(self.main, text="النتيجة",font = self.addressFont)
        id_label = ttk.Label(self.main, text=f"{Global_var.mil_id} :الرقم العسكري",font = self.labelFont).place(x = 240,y = 50)
        name_label = ttk.Label(self.main, text=f"الاسم: {Global_var.name}",font = self.labelFont).place(x = 260,y = 75)
        
        label1 = ttk.Label(self.main, text=":المحاولة التجريبية",font = self.labelFont).place(x=380, y= 100)
        num1 = ttk.Label(self.main, text=self.data_trial,font = self.labelFont).place(x=340, y= 100)                      
        label2 = ttk.Label(self.main, text=":المحاولة الاختبارية",font = self.labelFont).place(x=380, y= 125)
        num2 = ttk.Label(self.main, text=self.data_test[0],font = self.labelFont).place(x=340, y= 125)
        label2 = ttk.Label(self.main, text=":المحاولة الاختبارية*2",font = self.labelFont).place(x=360, y= 150)
        num2 = ttk.Label(self.main, text=self.data_test[1],font = self.labelFont).place(x=340, y= 150)   
        adress_label.place(x=250, y=15)
        res_label = ttk.Label(self.main, text=f"{self.data_test[2]} :الدرجة",font = self.addressFont).place(x = 350,y = 175)
        restart_test_btn =  ttk.Button(self.main,text="حفظ",width=10, command=self.submit).place(x= 280,y = 225)  

    def formulate_data(self):
        data = {
                "id":Global_var.mil_id,
                "name":Global_var.name,
                'depthTrialTrain':self.data_trial, 
                'depthTrial1':self.data_test[0], 
                'depthTrial2':self.data_test[1], 
                'depthData':self.data_test[2], 
        }
        return data

    def submit(self):
        data = self.formulate_data()
        send_request(data,Global_var.ip,"arms")# CHANGE
        time.sleep(0.5)
        self.next_frame = GUI_Template.InforamtionPage(self.main,self,True)
        transete(self.main,self.next_frame)
        self.reset()
                        
root = ThemedTk(theme="breeze")
dp = DepthRecognintion(root)
master = GUI_Template.InforamtionPage(root,dp,True)
master.window()
root.mainloop()    
