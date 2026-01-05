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
import myportal.common as common


class listsHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
        else:
            # 统计模块开始
            conn = sqlite3.connect(
                "D:\\projects3\\db\\baigaopeng_myportal.db")
            sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'design_list')"
            result = conn.cursor().execute(sql)
            conn.commit()
            conn.close()
            common.tongji("design_lists")
            # 统计模块结束

            users = common.select("organization","select * from user")

            self.render("organization\\templates\\User\\lists.html",users=users)


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_Index_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render("organization/templates/index.html")
    def on_response(self,response):
        body= json.loads(response.body)
        print("response内容为:",body)
        self.finish


class checkPassHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(
            "D:\\projects3\\db\\baigaopeng_myportal.db")
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'check_pass')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        sql = "update user set status='checked' where id="+self.get_argument("id")
        designs = conn.cursor().execute(sql)
        conn.commit()
        self.write("修改成功！")