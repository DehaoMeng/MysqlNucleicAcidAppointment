#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：message 
@File    ：usermanager.py
@IDE     ：PyCharm 
@Author  ：昊昊
@Date    ：2022/6/21 下午 2:46
'''
import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import FindMessage as FM
import FindResult as FR
'''
        表数据
'''
datebase = "nucleicacidinformationbase"
usertable = "usertable"
locationtable = "samplingpointable"
resultable = "resultable"
messagetable = "appointmentable"
userName = "root"
pwd = "123456"
Time = ["09:00-12:00","14:00-17:00"]
Local = ["京江报告厅","大学生创业孵化基地","学苑楼","研究生报告厅"]
Date = ["2021-10-30","2021-10-31","2021-11-1","2021-11-2","2021-11-3","2021-11-1","2021-11-4","2021-11-5"]


class UserTkinter():
    def __init__(self):
        # 窗口设置。
        self.root = tk.Tk()
        self.root.title("预约")
        self.root.iconbitmap('./001.ico')
        # 画布搭建
        self.root.resizable(False,False)
        screenheight = self.root.winfo_screenheight()
        screenwidth = self.root.winfo_screenwidth()
        self.size = "%dx%d+%d+%d"%(400,250,(screenwidth-400)/2,(screenheight-250)/2)
        self.root.geometry(self.size)
        self.frame = tk.Frame(self.root,width=400,height=250)
        self.__menu()
        self.root.mainloop()

    def __menu(self):
        # 主界面
        self.label = None
        self.frame.place(x=0,y=0)
        SamplingpointLabel = tk.Label(self.frame,text="采样点:",width=10)
        SamplingpointLabel.place(x=10,y=10)
        self.SamplingpointChose = ttk.Combobox(self.frame)
        self.SamplingpointChose.place(x=80,y=10)
        self.SamplingpointChose["value"] = Local
        UserNameLable = tk.Label(self.frame,text="用户姓名:",width=10)
        UserNameLable.place(x=10,y=50)
        self.UserNameEntry= tk.Entry(self.frame,width=23,validate="focusout",validatecommand=self.__test)
        self.UserNameEntry.place(x=80,y=50)
        AuthenticationLabel = tk.Label(text="身份证号:")
        AuthenticationLabel.place(x=18,y=90)
        self.AuthenticationEntry = tk.Entry(self.frame,width=23,validate="focusout",validatecommand=self.__test)
        self.AuthenticationEntry.place(x=80,y=90)
        DateLable = tk.Label(self.frame,text="选择时间:")
        DateLable.place(x=18,y=130)
        self.DateChose = ttk.Combobox(self.frame)
        self.DateChose.place(x=80, y=130)
        self.DateChose["value"] = Date
        TimeLable = tk.Label(self.frame,text="选择时间:")
        TimeLable.place(x=18,y=170)
        self.TimeChose = ttk.Combobox(self.frame)
        self.TimeChose.place(x=80,y=170)
        self.TimeChose["value"]=Time
        SubmitCommit = tk.Button(self.frame,text="提交",width=20,command=self.__Submit,bg="green")
        SubmitCommit.place(x=80,y=210)
        tk.Button(self.frame,text="查询预约",command=self.__find,width=18,bg="green").place(x=250,y=175)
        tk.Button(self.frame,text="查看结果",command=self.__Result,width=18,bg="green").place(x=250,y=210)

    def __Result(self):
        username = self.UserNameEntry.get()
        auth = self.AuthenticationEntry.get()
        if not (username and auth):
            tk.messagebox.showerror(title="Error", message="请输入用户完整信息")
            return False
        FR.FindResult(auth)

    def __test(self):
        # 身份输入验证
        username = self.UserNameEntry.get()
        authentication = self.AuthenticationEntry.get()
        if username == "" or authentication == "":
            return True
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        cursor = conn.cursor()
        sql = 'select * from {} where Uname="{}" and Uno="{}"'.format(usertable, username, authentication)
        result = cursor.execute(sql)
        if result == 0:
            self.label = tk.Label(self.frame, text="身份错误，请重新输入!")
            self.label.place(x=250, y=80)
        if result == 1:
            try:
                self.label.destroy()
            except AttributeError:
                pass
        cursor.close()
        conn.close()
        return True

    def __Submit(self):
        # 提交按钮
        Sno = self.__FindLocation()
        Uno = self.AuthenticationEntry.get()
        Timing = self.TimeChose.get()
        date = self.DateChose.get()
        if Timing not in Time:
            tk.messagebox.showerror(title="Error",message="请输入正确的时间")
            return False
        if  date not in Date:
            tk.messagebox.showerror(title="Error",message="请输入正确的日期")
            return False
        if not (Sno and Uno and date and Timing):
            tk.messagebox.showerror(title="Error",message="请输入完整信息")
            return False
        Code = self.__VerificationCode(Uno,Sno,date,Timing)
        if not Code:
            tk.messagebox.showerror(title="error",message="请勿重复预约！如有其他问题请联系管理员！")
            return
        sql = 'Insert into {} (Uno,Sno,AppointmentDate,Timing,VerificationCode) value ("{}", "{}", "{}", "{}","{}")'.format(messagetable,Uno,Sno,date,Timing,Code)
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        print(Code)
        cursor = conn.cursor()
        flag = cursor.execute(sql)
        if  flag== 1:
            conn.commit()
            tk.messagebox.showinfo(title="success",message="预约成功")
        else:
            conn.rollback()
            tk.messagebox.showerror(title="Error",message="预约失败")
        cursor.close()
        conn.close()

    def __FindLocation(self):
        # 查找采样点编号
        location = self.SamplingpointChose.get()
        if location not in Local:
            return
        sql = 'select Sno from {} where Sname="{}"'.format(locationtable,location)
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        cursor = conn.cursor()
        cursor.execute(sql)
        Sno = cursor.fetchone()
        cursor.close()
        conn.close()
        if Sno:
            return Sno[0]

    def __find(self):
        username = self.UserNameEntry.get()
        auth = self.AuthenticationEntry.get()
        if not (username and auth):
            tk.messagebox.showerror(title="Error",message="请输入用户完整信息")
            return False
        FM.FindMessageMenu(auth)

    def __VerificationCode(self,Uno,Sno,date,Timing):
        sql = 'select * from {} where Uno="{}" and Appointmentdate="{}"'.format(messagetable,Uno,date)
        conn = pymysql.connect(host="localhost", user=userName, password=pwd, database=datebase, charset="utf8")
        cursor = conn.cursor()
        if cursor.execute(sql) == 0:
            Code = Sno[-2:]+date[5:7]+date[8:10]
            if Timing == "09:00-12:00":
                Code += "0"
            else:
                Code += "1"
            cursor.execute('select VerificationCode from {} where AppointmentDate="{}" and Timing="{}" and Sno="{}" Order by VerificationCode DESC'.format(messagetable,date,Timing,Sno))
            num = cursor.fetchone()
            if num and Code[-1]==num[0][-6]:
                Code += '0'*(5-len(str(int(num[0][-5:])+1))) + str(int(num[0][-5:])+1)
            else:
                Code += "00001"
            return Code
        else:
            return None


if __name__ == "__main__":
    UserTkinter()