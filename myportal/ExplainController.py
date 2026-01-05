import tornado
import sqlite3
import time
import requests
import os
import myportal.common as common


class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("now is accessing myportal_holiday_doubleadd_get")
        self.render("myportal/templates/Holiday/add.html")
    def post(self):
        #print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        data["name"]=self.get_argument("name")
        data["content"]=self.get_argument("content")
        sql="insert into explain(`name`,content) values('"+data["name"]+"','"+data["content"]+"')"
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        self.write("添加成功！")
        
        
class doubleAddHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'explain_doubleAdd')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render("myportal/templates/Explain/add.html")
        
    def post(self):
        print("进入myportal_holiday_doubleadd_post方法了")
        
        #print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        data["name"]=self.get_argument("name")
        data["content"]=self.get_argument("content")
        sql="insert into explain(`name`,content) values('"+data["name"]+"','"+data["content"]+"')"
        print("sql sentence:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
                
        ##remote
        url1   ="http://192.168.43.1:8000/myportal/Home/Explain/add"
        res=requests.post(url1,data=data)
        print("http响应为:",res.content)
        self.write(res.content)

        #print("result结果为:",result)
        
class editHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'explain_edit')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        print("进入task_edit_get方法了")
        
    def post(self):
        print("进入task_edit_post方法了")

        data={}
        #data["start_display_time"] = self.get_argument("start_display_time")
        #data["start_display_time"] = str(int(time.mktime(time.strptime(self.get_argument("start_display_time"),"%Y,%m,%d,%H"))))
        #data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        #data["challenge"]=self.get_argument("challenge")
        #data["impede"]=self.get_argument("impede")
        #data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")

        sql = "update explain set id="+data["id"]
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        #sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        #sql=sql+",impede='"+self.get_argument("impede")+"' "
        #sql=sql+",address='"+",".join(self.get_arguments("address"))+"'"
        #print("地点post数据",self.get_arguments("address"))
        #sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        print("sql语句:"+sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        print("result结果为:",result)     
        self.write("")  
        
        #task的编辑模块
class doubleEditHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_explain_doubleAdd')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        print("进入explain_doubleedit_get方法了")
        sql="select * from explain where id="+self.get_argument("id")
        explain=common.find("baigaopeng_myportal",sql)
        explain["content"]=explain["content"].replace("&nbsp"," ").replace("<br>","\n")
        self.render("myportal/templates/explain/edit.html"
         
         ,explain=explain
        	)
        	
        	#在这对python和php对于模拟客户端发起http请求的处理方法的不同做一个说明
        	#php主要用作后端，一般不需要发起http请求，而是接收http请求。因此原生需要没有关于模拟浏览器发起http请求的功能是可以理解的。因此也就用到了curl这样的第三方类库
        	#而python是系统语言(或者用现在的说法是全栈语言)，可以需要对浏览器客户端进行开发，因此原生语言内置了模拟浏览器发起http请求的功能。就是client类。
        	#而它的使用和curl一样都是模拟了一个客户端类，用它的方法发起请求
    #@tornado.web.asynchronous
    def post(self):
        #print("post['address']:",self.get_arguments("address"))
        url1   ="http://192.168.43.1:8000/myportal/Home/Explain/edit?id="+self.get_argument("id")
       
        
        #data={'id':self.get_argument("id")}
        data={}
        #data["start_display_time"] = str(int(time.mktime(time.strptime(start_display_time,"%Y,%m,%d,%H"))))
        #data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        #data["challenge"]=self.get_argument("challenge")
        #data["impede"]=self.get_argument("impede")
        #data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")


        sql = "update explain set id="+data["id"]
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        #sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        #sql=sql+",impede='"+self.get_argument("impede")+"' "
        #sql=sql+",address='"+data["address"]+"'"
        #print("地点post数据",self.get_arguments("address"))
        #sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        print("sql语句:"+sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        print("result结果为:",result)
        
        res=requests.post(url1,data=data)
        print("http响应为:",res.content)
        self.write(res.content)
        


class listsHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_explain_lists')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        print("进入explain_list_get方法了")
        sql="select * from explain where status='abled'"
        explains=common.select("baigaopeng_myportal",sql)
        self.render("myportal/templates/Explain/lists.html"
        	,explains=explains)
    def post(self):
        print("进入holiday_list_post方法了")


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_explain_select')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        print("进入myportal_select_get方法了")

        self.render("myportal/templates/explain/select.html"
        	        	
        	)
        
    def post(self):
        #print("进入myportal_explain_select_post方法了")
        
        #print("post数据:"+self.get_argument(status"))
        sql="select * from explain where 1=1 "
        if self.get_argument("keyword1","空值")!="空值":
            sql=sql+" and (name like '%"+self.get_argument("keyword1")+"%' or \
        	 content like '%"+self.get_argument("keyword1")+"%' or \
        	 id like '%"+self.get_argument("keyword1")+"%' \
        	)"
        if self.get_argument("keyword2","nullvalue")!="nullvalue":
            sql=sql+" and (name like '%"+self.get_argument("keyword2")+"%' or \
        		content like '%"+self.get_argument("keyword2")+"%' or \
        		id like '%"+self.get_argument("keyword2")+"%' \
        		)"
        if self.get_argument("keyword3","nullvalue")!="nullvalue":
            sql=sql+" and (name like '%"+self.get_argument("keyword3")+"%' or \
        		content like '%"+self.get_argument("keyword3")+"%' or \
        		id like '%"+self.get_argument("keyword3")+"%' \
        		)"
        		
        sql=sql+" order by status asc"
        #print("sql is:",sql)
        explains=common.select("baigaopeng_myportal",sql)
        

        #print("explains is:",explains)
        #print("data is:",data)
        self.render("myportal/templates/explain/result.html"
        		,explains=explains)
    


class relationShipTreeHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_explain_select')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        sql="select * from explain_test where id="+self.get_argument("id")
        explain=common.find("baigaopeng_myportal",sql)
        i=0
        #parent_id=explain["parent_id"]
        relationship={}
        while explain["parent_id"]!=None:
            sql="select * from explain_test where id="+explain["parent_id"]
            explain=common.find(sql,"baigaopeng_myportal")
            relationship[i]=explain["name"]
            i=i+1
            #self.get_=explain["parent_id"]
        #print("进入myportal_select_get方法了")
        self.render("myportal/templates/Explain/relationship_tree.html"
        	,relationship=relationship
        	)
        
    def post(self):
        print("进入myportal_explain_select_post方法了")
        
        #print("post数据:"+self.get_argument(status"))
        sql="select * from explain where 1=1 "
        if self.get_argument("keyword1","空值")!="空值":
            sql=sql+" and (name like '%"+self.get_argument("keyword1")+"%' or \
        	 content like '%"+self.get_argument("keyword1")+"%' or \
        	 id like '%"+self.get_argument("keyword1")+"%' \
        	)"
        if self.get_argument("keyword2","nullvalue")!="nullvalue":
            sql=sql+" and (name like '%"+self.get_argument("keyword2")+"%' or \
        		content like '%"+self.get_argument("keyword2")+"%' or \
        		id like '%"+self.get_argument("keyword2")+"%' \
        		)"
        if self.get_argument("keyword3","nullvalue")!="nullvalue":
            sql=sql+" and (name like '%"+self.get_argument("keyword3")+"%' or \
        		content like '%"+self.get_argument("keyword3")+"%' or \
        		id like '%"+self.get_argument("keyword3")+"%' \
        		)"
        		
        sql=sql+" order by status asc"
        print("sql is:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_myportal.db")
        explains=conn.cursor().execute(sql)
        result=conn.commit()


        print("explains is:",explains)
        #print("data is:",data)
        self.render("myportal/templates/explain/result.html"
        		,explains=explains)
    


