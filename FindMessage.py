#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：message 
@File    ：FindMessage.py
@IDE     ：PyCharm 
@Author  ：昊昊
@Date    ：2022/6/24 0024 上午 8:24 
'''
import pymysql
import tkinter as tk
from PIL import Image,ImageTk
import qrcode
import warnings
from tkinter import messagebox
warnings.filterwarnings("ignore",category=DeprecationWarning)
datebase = "nucleicacidinformationbase"
usertable = "usertable"
locationtable = "samplingpointable"
resultable = "resultable"
messagetable = "appointmentable"
userName = "root"
pwd = "123456"
img_file = r'./img/'
class FindMessageMenu():
    def __init__(self,auth):
        # 查询预约界面
        sql = 'select AppointmentDate,Timing,VerificationCode from {} where Uno="{}" and Status="{}" Order by' \
              ' AppointmentDate '.format(messagetable, auth,"否")
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)
        self.messages = cursor.fetchone()
        cursor.close()
        conn.close()
        find = tk.Toplevel()
        find.title("查询预约")
        find.iconbitmap('./001.ico')
        find.resizable(False, False)
        screenheight = find.winfo_screenheight()
        screenwidth = find.winfo_screenwidth()
        size = "%dx%d+%d+%d" % (300, 250, (screenwidth - 300) / 2, (screenheight - 250) / 2)
        find.geometry(size)
        frame = tk.Frame(find, width=300, height=250)
        frame.place(x=0, y=0)
        frame1 = tk.Frame(frame, width=180, height=100)
        frame1.place(x=40, y=10)
        if not self.messages :
            tk.Label(frame1, text="当前用户无预约!!!!").place(x=50, y=25)
        else:
            messages = list(self.messages)
            message = str(messages[0]) + " " + messages[1] + "\r\n" +\
                           "当前尚未核验\r\n" + "您的验证码为: "
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=10,
                border=4
            )
            qr.add_data(messages[-1])
            img = qr.make_image()
            img.save(img_file+str(auth)+".png")
            tk.Label(frame1,text=message,wraplength=150).place(x=30,y=10)
            frame2 = tk.Frame(frame,width=100,height=100)
            frame2.place(x=100,y=110)
            img = ImageTk.PhotoImage(Image.open("./img/" + str(auth) +".png").resize((80,80),Image.ANTIALIAS))
            tk.Label(frame2,image=img).place(x=0,y=0)
        tk.Button(frame, text="Cannel", command=find.destroy).place(x=75, y=200)
        tk.Button(frame, text="取消预约", command=self.__Cannel).place(x=140, y=200)
        find.mainloop()

    def __Cannel(self):
        if tk.messagebox.askokcancel("Warin","确定取消预约吗？"):
            sql = 'Delete from {} where VerificationCode="{}"'.format(messagetable,self.messages[-1])
            conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            conn.close()


if __name__ == '__main__':
    FindMessageMenu(120223200204245552)