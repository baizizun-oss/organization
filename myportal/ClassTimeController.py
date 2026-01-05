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
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'class_time_add')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        print("now is accessing myportal_ClassTime_doubleadd_get")
        self.render("myportal/templates/ClassTime/add.html")
    def post(self):
        print("now is accessing myportal_ClassTime_doubleadd_post")
        data={}
        data["start_time"]=self.get_argument("start_time")
        data["end_time"]=self.get_argument("end_time")
        
        sql="insert into class_time(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        
        
class doubleAddHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'class_time_doubleAdd')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render("myportal/templates/ClassTime/add.html")
        
    def post(self):
        print("进入myportal_ClassTime_doubleadd_post方法了")
        
        #print("now is accessing myportal_ClassTime_doubleadd_post")
        data={}
        start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        
        
        sql="insert into class_time(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
                
        ##remote
        #url_another   ="http://192.168.43.1:8000/myportal/Home/ClassTime/add"
        url_another   ="http://"+common.get_ip()+"/myportal/Home/ClassTime/add"
        res=requests.post(url_another,data=data)
        print("http响应为:",res.content)
        self.write(res.content)
        

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'ClassTime_lists')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        ClassTimes=sqlite3.connect("projects3/db/baigaopeng_myportal.db").cursor().execute("select * from class_time")
        print("进入ClassTime_list_get方法了")
        self.render("myportal/templates/ClassTime/lists.html"
        	,class_times=ClassTimes)
    def post(self):
        print("进入ClassTime_list_post方法了")



class delHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'ClassTime_lists')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        #ClassTimes=sqlite3.connect("projects3/db/baigaopeng_myportal.db").cursor().execute("delete from class_time where id="+self.get_argument("id"))
        sql="delete from class_time where id="+self.get_argument("id")
        common.execute("baigaopeng_myportal",sql)
        self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>') 
    def post(self):
        print("进入ClassTime_list_post方法了")        


class doubleDelHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'ClassTime_lists')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        sql="delete from class_time where id="+self.get_argument("id")
        common.execute("baigaopeng_myportal",sql)
        #ClassTimes=sqlite3.connect("projects3/db/baigaopeng_myportal.db").cursor().execute("delete  from class_time where id="+self.get_argument("id"))
        self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>') 
        url_another   ="http://"+common.get_ip()+"/myportal/Home/ClassTime/del?id="+self.get_argument("id")
        res=requests.get(url_another)
        print("http响应为:",res.content)
        self.write(res.content)
    def post(self):
        print("进入ClassTime_list_post方法了")                       