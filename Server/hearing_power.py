# this module used to get inputs like height and weight to GUI

from cProfile import label
from ctypes import alignment
from sre_parse import expand_template
import tkinter as tk
import json
import requests
from flask import request
from tkinter import messagebox


    
main = tk.Tk()
main.geometry("600x310")

grades = ['غير لائق','مقبول','جيد','جيد جدا','امتياز']

adress_label = tk.Label(main, text="قياس شدة السمع",font = "arial 20 bold")
id_label = (tk.Label(main, text="الرقم العسكري")).place(x=415, y= 50)
id_text = tk.Text(main,height = 1,width=25)
id_text.place(x = 200,y = 50)
    
name_label = (tk.Label(main, text="الاسم",font = "arial 12")).place(x=415, y= 100)
name_text = tk.Text(main,height = 1,width=25)
name_text.place(x = 200,y = 100)
right_label = (tk.Label(main, text="الاذن اليمنى",font = "arial 12")).place(x=415, y= 150)
right_text = tk.Text(main,height = 1,width=4)
right_text.place(x = 370,y = 150)
left_label = (tk.Label(main, text="الاذن اليسرى",font = "arial 12")).place(x=240, y= 150)
left_text = tk.Text(main,height = 1,width=4)
left_text.place(x = 200,y = 150)
gradeR_label = (tk.Label(main, text=":نتيجة اليمنى",font = "arial 12")).place(x=415, y= 200)
gR_label = (tk.Label(main, text="",font = "arial 12"))
gR_label.place(x=375, y= 200)
gradeL_label = (tk.Label(main, text=":نتيجة اليسرى",font = "arial 12")).place(x=240, y= 200)
gL_label = (tk.Label(main, text="",font = "arial 12"))
gL_label.place(x=200, y= 200)
gradeL_num = None
gradeR_num = None
def validations(id, name, rg,lg):
    msg = ""
    flag = False
    try :
        if len(id) == 0 or len(name) == 0 or len(lg) == 0 or len(rg) == 0:
            msg =  "يجب ملئ كل الخانات"
        else:
            if any(not ch.isdigit() for ch in id):
                msg = 'الرقم العسكري لا يمكن ان يحتوي على حروف'
            elif len(id) != 13:
                msg = 'الرقم العسكري يجب ان يكون 13 رقم'
            elif any(ch.isdigit() for ch in name):
                msg = 'الاسم لا يحتوي على ارقام'
            elif any(not ch.isdigit() for ch in rg) or int(rg) < 0 or int(rg) > 4:
                msg = 'الدرجة خاطئة'
            elif any(not ch.isdigit() for ch in lg) or int(lg) < 0 or int(lg) > 4:
                msg = 'الدرجة خاطئة'
            else:
                flag = True
    except Exception as ep:
            messagebox.showerror('error', ep)
    if not flag:
        messagebox.showerror("خطأ", msg)
    return flag

def send_request(id,name,rg,lg):
    if gradeL_num is None or gradeR_num is None:
        messagebox.showerror('error', "قم بحساب النتيجة اولا")
        return
    data = {
        "id":int(id),
        "name":name,
        "right_grade":rg,
        "right_result":grades[rg],
        "left_grade":lg,
        "left_result":grades[lg]
    }
    serialized_data = json.dumps(data)
    headers = {
        "content-type": "application/json; charset=utf-8"
    }
    requests.post(url="http://localhost:5000/hearing", data=serialized_data, headers=headers)
        
def calculate_grade():
    global gradeL_num
    global gradeR_num
    id,name,rg,lg = get_data()
    flag = validations(id, name, rg,lg)
    if flag:
        gradeL_num = grades[int(lg)]
        gradeR_num = grades[int(rg)]
        
        gR_label.config(text = gradeR_num)
        gL_label.config(text = gradeL_num)
        print(gradeR_num, gradeL_num)

def get_data():
    id = id_text.get(1.0, "end-1c")
    name = name_text.get(1.0, "end-1c")
    rg = right_text.get(1.0, "end-1c")
    lg = left_text.get(1.0,"end-1c")
    return id,name,rg,lg

def submit():
    id,name,rg,lg = get_data()
    flag = validations(id, name, rg,lg)
    if flag:
        send_request(id, name, int(rg),int(lg))


calculate_button = tk.Button(main,text="حساب النتيجة",width=10,height=2, command=calculate_grade).place(x= 200,y = 250)
submit_button = tk.Button(main,text="حفظ",width=10,height=2, command=submit).place(x= 350,y = 250)
adress_label.pack()

main.mainloop()
