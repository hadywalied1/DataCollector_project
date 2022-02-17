import time
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as tkFont
from Helper_module import readCOM, writeCOM
import Global_var
from click import option
from Helper_module import validate_all_fields, validate_id, validate_name

from Helper_module import readIP, writeIP, get_inputs, reset_inputs,transete

class InforamtionPage:
    Global_var.init_globals()
    default_server_address = None
    Global_var.ip = default_server_address
    default_port_number = "5000"
    default_COMport = None
    next_frame = None
    arduino_flag = False
    def __init__(self, main,next_frame,arduino_flag = False):
        self.next_frame = next_frame
        self.main = main
        self.arduino_flag = arduino_flag
        self.main.geometry("600x300")
        self.main.title("تسجبل البيانات")
        self.main.minsize(600,300)
        self.main.maxsize(600,300)
    def window(self):
        self.default_server_address = readIP()
        self.default_COMport = readCOM()
        Global_var.ip = self.default_server_address
        Global_var.COMport = self.default_COMport
        addressFont = tkFont.Font(family="Andalus", size=20, weight="bold") 
        labelFont = tkFont.Font(family="Arabic Typesetting", size=16, weight="bold") 
        adress_label = ttk.Label(self.main, text="تسجيل بيانات المختبر",font = addressFont)
        adress_label.place(x=200, y=10)
        id_label = (ttk.Label(self.main, text="الرقم العسكري",font = labelFont)).place(x=430, y= 70)
        id_text = ttk.Entry(self.main,width=30)
        id_text.place(x = 190,y = 70)   
        name_label = (ttk.Label(self.main, text="الاسم",font = labelFont)).place(x=430, y= 120)
        name_text = ttk.Entry(self.main,width=30)
        name_text.place(x = 190,y = 120)
        menubar = tk.Menu(self.main)
        self.main.config(menu=menubar)
        # create a menu
        file_menu = tk.Menu(menubar)
        # add a menu item to the menu
        file_menu.add_command(
            label='IP',
            command=lambda: self.ip_window()
        )
        if self.arduino_flag:
            file_menu.add_command(
                label='COM port',
                command=lambda: self.COMport_window()
            )
        # add the File menu to the menubar
        menubar.add_cascade(
            label="الأعدادات",
            menu=file_menu
        )
        submit_button = ttk.Button(self.main,text="بدأ الاختبار",width=10, command=self.submit_main_data)
        submit_button.place(x= 250,y = 200)    
    
    def set_ip(self,ip_entry,win):
        ip= ip_entry.get()
        self.default_server_address = ip
        Global_var.ip = ip
        writeIP(ip)
        time.sleep(0.5)
        win.destroy()
    
    def set_com(self,com_entry):
        com= com_entry.get()
        self.default_server_address = com
        Global_var.COMport = com
        writeCOM(com)
                    
    def ip_window(self):
        ip_win = tk.Toplevel(self.main)
        ip_win.title("change IP")
        ip_win.geometry("250x100")
        ip_label = ttk.Label(ip_win, text="IP Address:",font = "calibri 12").place(x=10, y= 15)
        ip_text = ttk.Entry(ip_win,width=20)
        ip_text.delete(0, "end")
        ip_text.insert(0, self.default_server_address)
        ip_text.place(x=85, y= 10)
        ip_btn = ttk.Button(ip_win, text="حفظ",width=8, command=lambda: self.set_ip(ip_text,ip_win))
        ip_btn.place(x=100, y=60)

    def COMport_window(self):
        com_win = tk.Toplevel(self.main)
        com_win.title("change COM port")
        com_win.geometry("250x100")
        com_label = ttk.Label(com_win, text="port: COM",font = "calibri 12").place(x=10, y= 15)
        com_text = ttk.Entry(com_win,width=20)
        com_text.delete(0, "end")
        com_text.insert(0, self.default_COMport)
        com_text.place(x=85, y= 10)
        com_btn = ttk.Button(com_win, text="حفظ",width=8, command=lambda: self.set_com(com_text))
        com_btn.place(x=100, y=60)

    
    def submit_main_data(self):
        data = get_inputs(self.main)
        Flag,msg = self.validation(data)
        if not Flag:  
            messagebox.showerror("خطأ",msg)
        else:
            Global_var.mil_id = data[0]
            Global_var.name=data[1]
            transete(self.main,self.next_frame)
            reset_inputs(self.main)
            
            
    def validation(self,data):
        flag = True
        msg = ""
        if not validate_all_fields(data):
            msg = "يجب ملئ كل الخانات"
            flag = False
        elif not validate_id(data[0]):
            flag = False
            msg = 'الرقم العسكري يجب ان يكون 13 رقم ولا يحتوي على حروف'
        elif not validate_name(data[1]):
            flag = False
            msg = 'الاسم لا يحتوي على ارقام'
        return flag,msg
        

    
        
        
'''            
root = ThemedTk(theme="breeze")
main_gui = InforamtionPage(root)
root.mainloop()'''