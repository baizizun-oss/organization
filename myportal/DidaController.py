import tornado
import sqlite3
import time
import requests
##import androidhelper
from threading import Timer
import os
import datetime
from dateutil.relativedelta import relativedelta
import myportal.common as common
        

class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("now is accessing myportal_holiday_doubleadd_get")
        self.render("myportal/templates/Holiday/add.html")
    def post(self):
        
        #print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        data["start_time"] = self.get_argument("start_time")
        data["end_time"] = self.get_argument("end_time")
        #data["peroid"] = str(int(self.get_argument("peroid_year"))*365*24*60*60+int(self.get_argument("peroid_month"))*30*24*60*60+int(self.get_argument("peroid_day"))*24*60*60+int(self.get_argument("peroid_hour"))*60*60+int(self.get_argument("peroid_minute"))*60)
        data["peroid_year"] = str(int(self.get_argument("peroid_year")))
        data["peroid_month"]= str(int(self.get_argument("peroid_month")))
        data["peroid_day"]  = str(int(self.get_argument("peroid_day")))
        data["peroid_hour"] = str(int(self.get_argument("peroid_hour")))
        data["peroid_minute"]=str(int(self.get_argument("peroid_minute")))
        
        data["title"] = self.get_argument("title")
        
        sql="insert into dida(start_time,end_time,peroid_years,peroid_months,peroid_days,peroid_hours,peroid_minutes,title) values("+data["start_time"]+","+data["end_time"]+","+data["peroid_year"]+","+data["peroid_month"]+","+data["peroid_day"]+","+data["peroid_hour"]+","+data["peroid_minute"]+",'"+data["title"]+"')"
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        
        
class doubleAddHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("myportal/templates/Dida/add.html")
        
    def post(self):
        import time
        import sqlite3
        print("进入myportal_holiday_doubleAdd_post方法了")
        
        #print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        #next_time = str(int(self.get_argument("peroid_year"))+time.strftime("%Y"))+","+str(int(self.get_argument("peroid_month"))+time.strftime("%m"))+","+str(int(self.get_argument("peroid_day"))+time.strftime("%d"))+","+str(int(self.get_argument("peroid_hour"))+time.strftime("%H"))+","+str(int(self.get_argument("peroid_minute"))+time.strftime("%M"))
        #data["next_time"] = int(time.mktime(time.strptime(peroid,"%Y,%m,%d,%H,%M")))
        #data["peroid"] = data["next_time"] - time.mktime()
        data["peroid"] = str(int(self.get_argument("peroid_year"))*365*24*60*60+int(self.get_argument("peroid_month"))*30*24*60*60+int(self.get_argument("peroid_day"))*24*60*60+int(self.get_argument("peroid_hour"))*60*60+int(self.get_argument("peroid_minute"))*60)
        data["peroid_year"] = str(int(self.get_argument("peroid_year")))
        data["peroid_month"]= str(int(self.get_argument("peroid_month")))
        data["peroid_day"]  = str(int(self.get_argument("peroid_day")))
        data["peroid_hour"] = str(int(self.get_argument("peroid_hour")))
        data["peroid_minute"]=str(int(self.get_argument("peroid_minute")))
        
        data["title"] = self.get_argument("title")
        
        sql="insert into dida(start_time,end_time,peroid_years,peroid_months,peroid_days,peroid_hours,peroid_minutes,title) values("+data["start_time"]+","+data["end_time"]+","+data["peroid_year"]+","+data["peroid_month"]+","+data["peroid_day"]+","+data["peroid_hour"]+","+data["peroid_minute"]+",'"+data["title"]+"')"
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
                
        ##remote
        url1   ="http://192.168.43.1:8000/myportal/Home/Dida/add"
        res=requests.post(url1,data=data)
        #result1=os.system("python /storage/emulated/0/qpython/projects3/myportal/")


        ##import androidhelper
        import time
        import sqlite3
        from threading import Timer
        import datetime
        from dateutil.relativedelta import relativedelta


        droid = androidhelper.Android()


        #固定周期显示提醒内容
        def tixing(last_dida_time,peroid_years,peroid_months,peroid_days,peroid_hours,peroid_minutes,content):
            droid.ttsSpeak(content+"a83")
            print("当前时间"+time.strftime("%H%M")+"提醒内容"+content)
            droid.makeToast(content)
            droid.mediaPlay("/storage/emulated/0/qpython/projects3/myportal/templates/Dida/dida_pomo.ogg")
            filehandle=open("/storage/emulated/0/qpython/projects3/myportal/templates/Dida/record.txt","a")
            filehandle.write("\r\n当前时间"+time.strftime("%Y%m%d%H%M")+"提醒内容"+content)
            next_dida_time=(datetime.datetime.fromtimestamp(last_dida_time)+relativedelta(years=peroid_years)+relativedelta(months=peroid_months)+relativedelta(days=peroid_days)+relativedelta(hours=peroid_hours)+relativedelta(minutes=peroid_minutes)).timestamp()
            peroid=next_dida_time-last_dida_time
            Timer(peroid,tixing,args=(next_dida_time,peroid_years,peroid_months,peroid_days,peroid_hours,peroid_minutes,content)).start()



        #读取数据库
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        cursor=conn.cursor()
        sql="select * from dida"
        cursor.execute(sql)
        didas=cursor.fetchall()
        for row in didas:
            print(row)
            print("开始时间",row[1])
            print("结束时间",row[2])
            peroid_years=row[3]
            peroid_months=row[4]
            peroid_days    =row[5]
            peroid_hours   =row[6]
            peroid_minutes=row[7]
    
            next_dida_time=row[1]
            end_time=row[2]
            content=row[8]
    
            while time.time()>next_dida_time:
                #print("比较")
                next_dida_time=(datetime.datetime.fromtimestamp(next_dida_time)+relativedelta(years=peroid_years)+relativedelta(months=peroid_months)+relativedelta(days=peroid_days)+relativedelta(hours=peroid_hours)+relativedelta(minutes=peroid_minutes)).timestamp()
        
            Timer((next_dida_time-time.time()),tixing,args=(next_dida_time,peroid_years,peroid_months,peroid_days,peroid_hours,peroid_minutes,content)).start()

        
        
        print("http响应为:",res.content)
        self.write(res.content)
        

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入dida_list_get方法了")
        #print("didas:",didas)
        #print("didas:",didas.__dict__)
        didas=common.select("baigaopeng_myportal","select * from dida")
        for i in range(0,len(didas)):
            didas[i]["next_dida_time"]=didas[i]["start_time"]
            while time.time()>didas[i]["next_dida_time"]:
                #print("比较")
                didas[i]["next_dida_time"]=int((datetime.datetime.fromtimestamp(didas[i]["next_dida_time"])+relativedelta(years=didas[i]["peroid_years"])+relativedelta(months=didas[i]["peroid_months"])+relativedelta(days=didas[i]["peroid_days"])+relativedelta(hours=didas[i]["peroid_hours"])+relativedelta(minutes=didas[i]["peroid_minutes"])).timestamp())
        #print("didas[0]",didas[0])
        #冒泡法对二维数组重新排序
        '''
        for i in range(0,len(didas)):
            min_index=i
            #print("i",i)
            #print("didas",didas)
            for j in range(i+1,len(didas)):
                #print("didas['j']",didas[j])
                #print("j",j)
                if int(didas[min_index]["next_dida_time"])>int(didas[j]["next_dida_time"]):
                    min_index=j
            temp=didas[min_index]["next_dida_time"]
            didas[min_index]["next_dida_time"]=didas[i]["next_dida_time"]
            #print("temp",temp)
            #print("temp类型",type(temp))
            #print("didas[0]",didas[0])
            #print("didas[0]['next_dida_time']类型",type(didas[0]["next_dida_time"]))
            didas[i]["next_dida_time"]=temp
            '''
        #在数据模型中增加标题字段
        for i in range(0,len(didas)):
            if didas[i]["title"].split("》")[0]=="《任务笔记系统":
                task=common.find("baigaopeng_task","select * from task where id="+didas[i]["title"].split("》")[1])
            if didas[i]["title"].split("》")[0]=="《任务笔记系统开发版":
                task=common.find("baigaopeng_task_develop","select * from task where id="+didas[i]["title"].split("》")[1])
            if didas[i]["title"].split("》")[0]=="《任务笔记系统开发版测试版":
                task=common.find("baigaopeng_task_develop_test","select * from task where id="+didas[i]["title"].split("》")[1])
            didas[i]["task_title"]=task["title"]
        self.render("myportal/templates/Dida/lists.html"
        #,holidays=holidays
        ,didas=didas
        )
    def post(self):
        print("进入holiday_list_post方法了")


class delHandler(tornado.web.RequestHandler):
    def get(self):

        print("now is accessing myportal_holiday_doubleDel_post")
        sql="delete from dida where id="+self.get_argument("id")
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
        

class doubleDelHandler(tornado.web.RequestHandler):
    def get(self):
        
        print("进入myportal_holiday_doubleDel_post方法了")
        
        sql="delete from dida where id="+self.get_argument("id")
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
                
        ##remote
        url1   ="http://"+common.get_ip()+"/myportal/Home/Dida/del?id="+self.get_argument("id")
        res=requests.get(url1)
        print("http响应为:",res.content)
        self.write(res.content)
        
