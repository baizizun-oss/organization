# -*-coding:utf8;-*-
# qpy:console


import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import time
import random
import http.client
import json
import sqlite3
import re
import myportal.common as common

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_Index_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束

        self.render("organization\\templates\\Publicity\\index.html")



class loginHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_Index_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        #登录判断
        if self.get_cookie("student","") == "":#如果没有cookie说明还没有登录
            self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","index.html"))

    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            # print("post_data:",post_data)
        #print("post_data:", post_data)
        data = {}

        data["username"] = self.get_argument("username")
        data["password"] = self.get_argument("password")

        #sql = "insert into student(name,grade,class) values('" + data["username"] + "','"    + data["password"] + "')"
        sql = "select * from user where nickname='"+data["username"]+"' and password = '"+data["password"]+"'"
        #print(sql)
        user = common.select("organization",sql)
        #print(user)
        #print(user[0]["id"])
        # self.set_cookie("username", data["username"])

        # self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","index.html"))
        # #self.redirect("index.html")
        if user[0]["id"]!=None:
            self.set_cookie("user_id",str(user[0]["id"]),expires=time.time()+300)
            # self.set_cookie("status","已登录")
            self.write("登录成功！")
            self.render("organization/templates/Index/lists.html")
        else:
            self.write("密码错误或者账号不存在，请重新<a href='/organization/Index/login'>登录</a>！")



class registerHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_Index_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render("organization/templates/Index/register.html")

    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            # print("post_data:",post_data)
        print("post_data:", post_data)
        data = {}

        data["username"] = self.get_argument("username")
        data["password"] = self.get_argument("password")
        data["campus"] = self.get_argument("campus")
        data["class"] = self.get_argument("class")
        data["name"] = self.get_argument("name")

        #输入验证
        print("匹配结果：",re.match(r"[0-9]",data["name"]))
        if data["name"] == "" or data["username"] == "":#如果必须的字段为空
            self.write('<html><head><title>警告</title></head><body><script type="text/javascript">window.alert("请输入用户名和真实姓名！");window.location.href = "register";</script></body></html>')
            return
        if data["password"] == "":
            self.write('<html><head><title>警告</title></head><body><script type="text/javascript">window.alert("请设置密码！");window.location.href = "register";</script></body></html>')
            return
        if re.match(r"[0-9]",data["name"]) or re.match(r"[a-z]",data["name"]) or re.match(r"[A-Z]",data["name"]):
            self.write('<html><head><title>警告</title></head><body><script type="text/javascript">window.alert("名字不要乱写！");window.location.href = "register";</script></body></html>')
            return
        # if re.match(r"[x{4e00}-x{9fa5}]{2,5}",data["name"]):
        #     pass
        # else:
        #     self.write('<html><head><title>警告</title></head><body><script type="text/javascript">window.alert("名字不要乱写！");window.location.href = "register";</script></body></html>')
        #避免同名账号
        sql = "select * from user where nickname='"+data["username"]+"'"
        users=common.select("organization",sql)
        if users[0]["id"]:
            self.write('<html><head><title>警告</title></head><body><script type="text/javascript">window.alert("此账号已经被注册！");window.location.href = "register";</script></body></html>')
            return
        

        sql = "insert into user(nickname,password,campus,class,name,status) values('"+data["username"]+"','"+data["password"]+"','"+data["campus"]+"',"+data["class"]+",'"+data["name"]+"','未授权')"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        result=cursor.execute(sql)
        conn.commit()
        print(result)
        if result!=None:
            self.write('<html><head><title>提示</title></head><body><script type="text/javascript">window.alert("注册成功！可以登录了！");window.location.href = "login";</script></body></html>')




class clickSelectHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'click_select')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        print("now is accessing myportal_index_click_select_get")
        self.render("myportal/templates/Index/click_select.html")

    def post(self):
        print("now is accessing myporta_index_click_select_post")
        data = {}
        # start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        # data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        # end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        # data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        # data["start_time"]=self.get_argument("start_time")
        # data["end_time"]=self.get_argument("end_time")

        # sql="insert into holiday(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        sql = "select count(*) as fangwen_num,click_action from click group by click_action"
        print("sql sentence:", sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():  # 从fetchall中读取操作 print(row)
            print("result:", row)
            # self.write(row)
        conn.commit()
        conn.close()
        # self.write("添加成功！")
        # self.write(result)

