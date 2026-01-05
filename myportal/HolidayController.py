import tornado
import sqlite3
import time
import requests
import os
import myportal.common as common

if os.path.exists("/storage/emulated/0/qpython/projects3/192.168.43.178"):
    ip   ="http://192.168.43.1:8000"
if os.path.exists("/storage/emulated/0/qpython/projects3/192.168.43.123"):
    ip   ="http://192.168.43.1:8000"



class addHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'holiday_add')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        print("now is accessing myportal_holiday_doubleadd_get")
        self.render("myportal/templates/Holiday/add.html")
    def post(self):
        print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        #start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        #data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        #end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        #data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        data["start_time"]=self.get_argument("start_time")
        data["end_time"]=self.get_argument("end_time")
        
        sql="insert into holiday(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        print("sql sentence:",sql)
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
        
        
class doubleAddHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'holiday_doubleAdd')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render("myportal/templates/Holiday/add.html")
        
    def post(self):
        print("进入myportal_holiday_doubleadd_post方法了")
        
        #print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        
        
        sql="insert into holiday(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        print("sql sentence:",sql)
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
                
        ##remote
        #url_another   ="http://192.168.43.1:8000/myportal/Home/Holiday/add"
        url_another   ="http://"+common.get_ip()+"/myportal/Home/Holiday/add"
        res=requests.post(url_another,data=data)
        print("http响应为:",res.content)
        self.write(res.content)
        

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'holiday_lists')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        holidays=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from holiday")
        print("进入holiday_list_get方法了")
        self.render("myportal/templates/Holiday/lists.html"
        	,holidays=holidays)
    def post(self):
        print("进入holiday_list_post方法了")