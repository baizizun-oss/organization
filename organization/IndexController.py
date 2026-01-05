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
import datetime



def month_begin_timestamp():
    today = datetime.date.today()
    return datetime.datetime(year=today.year, month=today.month, day=1).timestamp()
def month_end_timestamp():
    today = datetime.date.today()
    next_month = (today.month ) % 12 +1
    year = today.year + ((next_month == 0) and 1 or 0)
    return datetime.datetime(year=year, month=next_month, day=1).timestamp()



class loginHandler(tornado.web.RequestHandler):

    def month_begin_timestamp():
        today = datetime.date.today()
        return datetime.datetime(year=today.year, month=today.month, day=1).timestamp()
    def month_end_timestamp():
        today = datetime.date.today()
        next_month = (today.month + 1) % 12
        year = today.year + ((next_month == 0) and 1 or 0)
        return datetime.datetime(year=year, month=next_month, day=1).timestamp()


    def get(self):

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
        print("post_data:", post_data)
        data = {}

        data["username"] = self.get_argument("username")
        data["password"] = self.get_argument("password")
        print("数据：",data)
        sql = "select * from user where nickname='"+data["username"]+"'"
        user = common.select("organization",sql)
        print("user:",user)
        if user[0]["id"]==None:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("账号不存在，请注册！");</script></body></html>')  
        else: 
            sql = "select * from user where nickname='"+data["username"]+"' and password = '"+data["password"]+"'"
            user = common.select("organization",sql)            
            if user[0]["id"]==None:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("密码错误，请重新输入！");</script></body></html>')  
            else:
                if user[0]["status"] == '未授权':
                    self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("还未审核，请联系白老师！");</script></body></html>')
                elif user[0]["status"] == '已被除名':
                    self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("连续三次缺勤，根据社团决议已被除名！");</script></body></html>')                    
                elif user[0]["status"] == 'disabled':
                    self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("你的账号不可用，请联系白老师！");</script></body></html>') 
                else:
                    self.set_cookie("user_id",str(user[0]["id"]),expires=time.time()+3000)
                    # self.set_cookie("status","已登录")
                    #签到模块开始
                    conn=sqlite3.connect(os.path.join("db","organization.db"))
                    sql="insert into click(user_id,click_time,click_action) values("+str(user[0]["id"])+","+str(int(time.time()))+",'myportal_Index_index')"
                    result=conn.cursor().execute(sql)
                    conn.commit()
                    conn.close()
                    #模块结束                    
                    self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("登录成功！");</script></body></html>')
                    
                    sql = "select sum(score) as month_score from user_score_history where user_id="+str(user[0]["id"])+ " and ctime >= "+ str(month_begin_timestamp()) + " and ctime <= " + str(month_end_timestamp())              
                    month_score = common.select("organization",sql)
                    sql= "select sum(score) as sum_score from user_score_history where user_id="+str(user[0]["id"])
                    score=common.select("organization",sql)
                    sql = "select points from user where id="+str(user[0]["id"])
                    historical_score= common.select("organization",sql)
                    print("type:",type(score[0]["sum_score"]),type(historical_score[0]["points"]))
                    
                    if score[0]["sum_score"] is None:
                        score[0]["sum_score"]=0
                    if month_score[0]["month_score"] is None:
                        month_score[0]["month_score"]=0                        
                    self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","index.html"),user_id=user[0]["id"],month_score=month_score[0]["month_score"],sum_score=score[0]["sum_score"]+historical_score[0]["points"])


            
class registerHandler(tornado.web.RequestHandler):
    def get(self):
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
        data["id_card"]=self.get_argument("id_card")
        data["type"]=self.get_argument("type")

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
        

        sql = "insert into user(nickname,password,campus,class,name,status,type,id_card) values('"+data["username"]+"','"+data["password"]+"','"+data["campus"]+"',"+data["class"]+",'"+data["name"]+"','未授权','"+data["type"]+"','"+data["id_card"]+"')"
        print(sql)
        conn = sqlite3.connect(os.path.join("db","organization.db"))
        cursor = conn.cursor()
        result=cursor.execute(sql)
        conn.commit()
        print(result)
        if result!=None:
            self.write('<html><head><title>提示</title></head><body><script type="text/javascript">window.alert("注册成功！可以登录了！");window.location.href = "login";</script></body></html>')



class clickStatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        #strftime的部分是实现将所有记录的点击时间都按照日期（去掉小时和分钟）取出，并根据这个日期来合并取出
        sql = "select click.id as id,click.click_time,click.click_action,user.name as name,strftime('%Y-%m-%d',datetime(click_time,'unixepoch')) as date_group from click,user where click.user_id=user.id and user.id="+self.get_argument("user_id") + " group by date_group"
        clicks=common.select("organization",sql)
        self.render("organization/templates/Index/click_statistics.html",clicks=clicks,name=clicks[0]["name"])