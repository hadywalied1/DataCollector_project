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
main.geometry("600x300")



adress_label = tk.Label(main, text="تسجيل الطول و الوزن",font = "arial 20 bold")
id_label = (tk.Label(main, text="الرقم العسكري")).place(x=430, y= 50)
id_text = tk.Text(main,height = 1,width=25)
id_text.place(x = 200,y = 50)
    
name_label = (tk.Label(main, text="الاسم",font = "arial 12")).place(x=430, y= 100)
name_text = tk.Text(main,height = 1,width=25)
name_text.place(x = 200,y = 100)
height_label = (tk.Label(main, text="الطول",font = "arial 12")).place(x=430, y= 150)
height_text = tk.Text(main,height = 1,width=5)
height_text.place(x = 360,y = 150)
weight_label = (tk.Label(main, text="الوزن",font = "arial 12")).place(x=260, y= 150)
weight_text = tk.Text(main,height = 1,width=5)
weight_text.place(x = 200,y = 150)
hUint_label = tk.Label(main, text= "سم", font= "arial 12").place(x=330, y=150)
wUint_label = tk.Label(main, text= "كجم", font= "arial 12").place(x=170, y=150)

def validations(id, name, height, weight):
    msg = ""
    flag = False
    try :
        if len(id) == 0 or len(name) == 0 or len(height) == 0 or len(weight) == 0:
            msg =  "يجب ملئ كل الخانات"
        else:
            if any(not ch.isdigit() for ch in id):
                msg = 'الرقم العسكري لا يمكن ان يحتوي على حروف'
            elif len(id) != 13:
                msg = 'الرقم العسكري يجب ان يكون 13 رقم'
            elif any(ch.isdigit() for ch in name):
                msg = 'الاسم لا يحتوي على ارقام'
            elif any(not ch.isdigit() for ch in height) or int(height) > 250 or int(height) < 70:
                msg = 'الطول خاطئ'
            elif any(not ch.isdigit() for ch in weight) or int(weight) > 250 or int(weight)< 30:
                msg = 'الوزن خاطئ'
            else:
                flag = True
    except Exception as ep:
            messagebox.showerror('error', ep)
    if flag:
        data = {
            "id":int(id),
            "name":name,
            "height":int(height),
            "weight":int(weight)
        }
        serialized_data = json.dumps(data)
        headers = {
            "content-type": "application/json; charset=utf-8"
        }
        requests.post(url="http://localhost:5000/weightHeight", data=serialized_data, headers=headers)
    else:
        messagebox.showerror("خطأ",msg)


def get_data():
    id = id_text.get(1.0, "end-1c")
    name = name_text.get(1.0, "end-1c")
    height = height_text.get(1.0, "end-1c")
    weight = weight_text.get(1.0, "end-1c")
    
    validations(id, name, height, weight)
    


submit_button = tk.Button(main,text="حفظ",width=10,height=2, command=get_data).place(x= 280,y = 200)

adress_label.pack()

main.mainloop()
