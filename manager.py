#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：message 
@File    ：manager.py
@IDE     ：PyCharm 
@Author  ：昊昊
@Date    ：2022/6/22 上午 12:17
'''
import tkinter as tk
from tkinter import messagebox
import pymysql
datebase = "nucleicacidinformationbase"
messagetable = "appointmentable"
resultable = "resultable"
userName = "root"
pwd = "123456"

class DocterMenu():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("医生管理系统")
        self.root.resizable(False, False)
        screenheight = self.root.winfo_screenheight()
        screenwidth = self.root.winfo_screenwidth()
        self.size = "%dx%d+%d+%d" % (300, 200, (screenwidth - 300) / 2, (screenheight - 200) / 2)
        self.root.geometry(self.size)
        self.frame = tk.Frame(self.root, width=300, height=200)
        self.__menu()
        self.frame.place(x=0,y=0)
        self.root.mainloop()

    def __menu(self):
        self.CodeLable = tk.Label(self.frame,text="核验码:",width=10,font=("heiti",20))
        self.CodeLable.place(x=0,y=30)
        self.CodeEntry = tk.Entry(self.frame,width=10,font=("heiti",20))
        self.CodeEntry.place(x=120,y=30,height=30)
        self.ResultLable = tk.Label(self.frame,text="结  果:",width=10,font=("heiti",20))
        self.ResultLable.place(x=0,y=80)
        self.ResultEntry = tk.Entry(self.frame,font=("heiti",20),width=10)
        self.ResultEntry.place(x=120,y=80,height=30)
        Submit = tk.Button(self.frame,text="提交",command=self.__Submit,font=("heiti",20))
        Submit.place(x=100,y=120)

    def __Submit(self):
        Code = self.CodeEntry.get()
        Result = self.ResultEntry.get()
        sql = 'select * from {} where VerificationCode="{}"'.format(messagetable,Code)
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        cursor = conn.cursor()
        flag = cursor.execute(sql)
        if flag == 0:
            tk.messagebox.showerror("请校对核验码！")
        else:
            sql = 'Insert into {} value ("{}","{}")'.format(resultable,Code,Result)
            try:
                cursor.execute(sql)
                conn.commit()
                tk.messagebox.showinfo(title="Success",message="录入成功")
            except:
                conn.rollback()
                tk.messagebox.showerror(title="Error",message="请勿重复录入！")
        cursor.close()
        conn.close()


if __name__ == "__main__":
    DocterMenu()