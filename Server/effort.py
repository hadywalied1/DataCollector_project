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



adress_label = tk.Label(main, text="عجلة بذل الجهد",font = "arial 20 bold")
id_label = (tk.Label(main, text="الرقم العسكري")).place(x=415, y= 50)
id_text = tk.Text(main,height = 1,width=25)
id_text.place(x = 200,y = 50)
    
name_label = (tk.Label(main, text="الاسم",font = "arial 12")).place(x=415, y= 100)
name_text = tk.Text(main,height = 1,width=25)
name_text.place(x = 200,y = 100)
heart_label = (tk.Label(main, text="دقات القلب",font = "arial 12")).place(x=415, y= 150)
heart_text = tk.Text(main,height = 1,width=10)
heart_text.place(x = 320,y = 150)

def validations(id, name, heart_rate):
    msg = ""
    flag = False
    try :
        if len(id) == 0 or len(name) == 0 or len(heart_rate) == 0:
            msg =  "يجب ملئ كل الخانات"
        else:
            if any(not ch.isdigit() for ch in id):
                msg = 'الرقم العسكري لا يمكن ان يحتوي على حروف'
            elif len(id) != 13:
                msg = 'الرقم العسكري يجب ان يكون 13 رقم'
            elif any(ch.isdigit() for ch in name):
                msg = 'الاسم لا يحتوي على ارقام'
            elif any(not ch.isdigit() for ch in heart_rate) or int(heart_rate) > 250 or int(heart_rate)< 10:
                msg = 'دقات القلب خاطئة'
            else:
                flag = True
    except Exception as ep:
            messagebox.showerror('error', ep)
    if flag:
        data = {
            "id":int(id),
            "name":name,
            "heart_rate":int(heart_rate),
        }
        serialized_data = json.dumps(data)
        headers = {
            "content-type": "application/json; charset=utf-8"
        }
        requests.post(url="http://localhost:5000/effortMeasure", data=serialized_data, headers=headers)
    else:
        messagebox.showerror("خطأ",msg)


def get_data():
    id = id_text.get(1.0, "end-1c")
    name = name_text.get(1.0, "end-1c")
    heart_rate = heart_text.get(1.0, "end-1c")
    
    validations(id, name, heart_rate)
    



submit_button = tk.Button(main,text="حفظ",width=10,height=2, command=get_data).place(x= 280,y = 200)

adress_label.pack()

main.mainloop()
