import os
import sys
import tkinter as tk
from tkinter import messagebox
import requests
import json
# this function used to read saved IP from 
# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)
    
def readIP():
    ip = None
    try:
        p = os.path.join(application_path,"defaultIP.txt")
        file = open(p,'r')
        ip = file.readline()
        file.close()
    except Exception:
        ip = "127.0.0.1"
    return ip

# this function used to write the new ip setting sto defaultP.txt file
def writeIP(ip):
    p = os.path.join(application_path,"defaultIP.txt")
    file = open(p,"w+")
    file.write(ip)
    file.close()

# this function used to read saved IP from 
def readCOM():
    com = None
    try:
        p = os.path.join(application_path,"defaultCOM.txt")
        file = open(p,'r')
        com = file.readline()
        file.close()
    except Exception:
        com = "4"
    return com

# this function used to write the new ip setting sto defaultP.txt file
def writeCOM(com):
    p = os.path.join(application_path,"defaultCOM.txt")
    file = open(p,"w+")
    file.write(com)
    file.close()
    
# This function used to reset all inputs in GUI
def reset_inputs(frame):
    children_widgets = frame.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'Entry':
            child_widget.delete(0, tk.END)

# This function used to clear frame 
def clear_window(frame):
    for window in frame.winfo_children():
        window.destroy()

def transete(frame,nextWindow):
    clear_window(frame)
    nextWindow.window()

# This function used to get all data from tkinter frame
def get_inputs(frame):
    data =[]
    children_widgets = frame.winfo_children()
    for child_widget in children_widgets:
        if child_widget.winfo_class() == 'TEntry':
            data.append(child_widget.get())
            
    return data

def validate_all_fields(data):
    flag = True
    for element in data:
        if len(element) == 0:
            flag = False
    return flag

def validate_id(id):
    flag = True
    if len(id) != 13:
        flag = False
    elif any(not ch.isdigit() for ch in id):
        flag = False
    return flag

def validate_name(name):
    flag = True
    if any(ch.isdigit() for ch in name):
        flag = False
    return flag

def validate_range(num,start,end):
    if any(not ch.isdigit() for ch in num) or int(num) > end or int(num) < start:
        return False
    return True

def send_request(data,ip,api):
        serialized_data = json.dumps(data)
        headers = {
            "content-type": "application/json; charset=utf-8"
        }
        try:
            r = requests.post(url=f"http://{ip}:5000/{api}", data=serialized_data, headers=headers)
            data = r.json()
            if (data['status'] == True):
                messagebox.showinfo("عملية ناجحة","تم حفظ النتيجة")
            else:
                messagebox.showerror("خطأ","قم باعادة الاختبار مرة اخرى وتاكد من ملئ البيانات بطريقة صحيحة")
        except Exception as e:
            print(e)
            messagebox.showerror("خطأ","حدثت مشكلة بالشبكة تاكد من عنوان الخادم او ان الاجهزة متصلة")
  