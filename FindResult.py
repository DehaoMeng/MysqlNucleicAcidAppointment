#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：message 
@File    ：FindResult.py
@IDE     ：PyCharm 
@Author  ：昊昊
@Date    ：2022/6/24 0024 上午 9:28 
'''
import tkinter as tk
import pymysql
from PIL import Image,ImageTk
datebase = "nucleicacidinformationbase"
usertable = "usertable"
locationtable = "samplingpointable"
resultable = "resultable"
messagetable = "appointmentable"
userName = "root"
pwd = "123456"
class FindResult():
    def __init__(self,auth):
         self.auth = auth
         Tk = tk.Toplevel()
         Tk.geometry("300x200")
         Tk.title("结果")
         Tk.iconbitmap('./001.ico')
         Tk.resizable(False,False)
         resultmessage = self.__FindVerCode()
         if not resultmessage[0]:
             message = "该用户暂时 "+resultmessage[1]
             tk.Label(Tk, text=message, wraplength=150).place(x=90, y=80)
         else:
             message = str(resultmessage[0][0]) + " " + resultmessage[0][1] + "\r\n" + \
                            "当前已核验\r\n" + "您的结果为: " + resultmessage[1][0]
             img = ImageTk.PhotoImage(Image.open("./img/" + str(auth) +".png").resize((80,80),Image.ANTIALIAS))
             tk.Label(Tk, image=img).place(x=110, y=90)
             tk.Label(Tk,text=message,wraplength=150).place(x=80,y=0)
         tk.mainloop()

    def __FindVerCode(self):
        sql = 'select AppointmentDate,Timing,VerificationCode from {} where Uno="{}" and Status="{}" Order by' \
              ' AppointmentDate DESC'.format(messagetable, self.auth, "是")
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)
        message = cursor.fetchone()
        if not message:
            result = "尚无结果"
            return message,result
        sql1 = 'select Result from {} where VerificationCode="{}"'.format(resultable,message[-1])
        cursor.execute(sql1)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return message,result