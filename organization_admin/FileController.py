import tornado
import sqlite3
import urllib
import requests
import warnings
warnings.filterwarnings('ignore')
import time
import myportal.common as common
import os


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'fileserver_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        # if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
        #     print("没有cookie")
        #     self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
        #     #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        # else:
        #     self.render("fileserver/templates/index.html")
        self.render("fileserver/templates/index.html")

class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
    def post(self):

        data={}
        data["start_display_time"] = self.get_argument("start_display_time")
        data["title"]              = self.get_argument("title")
        data["content"]            = self.get_argument("content")
        data["address"]            = self.get_argument("address")
        data["status"]             = self.get_argument("status")
        data["ctime"]              = self.get_argument("ctime")
        data["remainder_time"]     = self.get_argument("remainder_time")
        data["type"]               = self.get_argument("type")


        sql="insert into task(title,content,address,\
        	status,start_display_time,ctime,remainder_time,type) values('"+data["title"]+"' \
        	,'"+data["content"]+"','"+data["address"]+"' \
        	,'"+data["status"]+"',"+data["start_display_time"]+" \
        	,"+data["ctime"]+" \
        	,"+data["remainder_time"]+" \
        	,'"+data["type"]+"' \
        	)"
        print("sql语句:"+sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        result=conn.cursor().execute(sql)
        print("result:",result)
                


        
class delHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        sql="delete from file where id="+self.get_argument("id")
        result=common.execute("baigaopeng_fileserver",sql)
        print("result结果为:",result)
        print("sql语句:"+sql)

                        
class downloadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","File","download.html"))
    def post(self):
        files=[]
        for i in range(self.get_argument("file_number")):
            sql="select * from file where easy_memorize_name='"+self.get_argument("easy_memorize_name")+"part"+str(i).zfill(len(self.get_argument("file_number")))+"'"
            print("sql:",sql)

            file=common.find("organization",sql)
            
            
            files.append(file)
        

                        

        
class editHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_edit_get方法了")
        
    def post(self):
        print("进入fileserver_edit_post方法了")

        data={}
        data["start_display_time"] = self.get_argument("start_display_time")
        #data["start_display_time"] = str(int(time.mktime(time.strptime(self.get_argument("start_display_time"),"%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"]=self.get_argument("challenge")
        data["impede"]=self.get_argument("impede")
        data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")

        sql = "update task set title='"+data["title"]+"'"
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        sql=sql+",impede='"+self.get_argument("impede")+"' "
        sql=sql+",address='"+",".join(self.get_arguments("address"))+"'"
        print("地点post数据",self.get_arguments("address"))
        sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        print("sql语句:"+sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        print("result结果为:",result)     
        self.write("")  
        
        #fileserver的编辑模块
class doubleEditHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_doubleedit_get方法了")
        files=sqlite3.connect("projects3/db/baigaopeng_fileserver.db").cursor().execute("select * from file where id="+self.get_argument("id"))
        for vo in files:
            file=vo
        #print("challenges:",dir(challenges))
      
        
        self.render("fileserver/templates/edit.html"
        	,file=file
        	)
        	
        	#在这对python和php对于模拟客户端发起http请求的处理方法的不同做一个说明
        	#php主要用作后端，一般不需要发起http请求，而是接收http请求。因此原生需要没有关于模拟浏览器发起http请求的功能是可以理解的。因此也就用到了curl这样的第三方类库
        	#而python是系统语言(或者用现在的说法是全栈语言)，可以需要对浏览器客户端进行开发，因此原生语言内置了模拟浏览器发起http请求的功能。就是client类。
        	#而它的使用和curl一样都是模拟了一个客户端类，用它的方法发起请求
    #@tornado.web.asynchronous
    def post(self):
        print("post['address']:",self.get_arguments("address"))
        #print("post数据:",self.get_argument())
        url1   ="http://192.168.43.1:8000/fileserver/Home/Index/edit?id="+self.get_argument("id")
        url123 ="http://127.0.0.1:8000/fileserver/edit?id="+self.get_argument("id")
        url_test="http://192.168.43.1:8080/fileserver/index.php?m=Home&c=index&a=doubleedit&id="+self.get_argument("id")
        
        #data={"id":self.get_arguments("id")}
        if self.get_argument("start_display_time_first_half") == time.strftime("%d"):
            start_display_time_day=self.get_argument("start_display_time_second_half")
        else:
            start_display_time_day=self.get_argument("start_display_time_first_half")
        if self.get_argument("start_display_time_morning")==time.strftime("%H"):
            start_display_time_hour=self.get_argument("start_display_time_afternoon")
        else:
            	start_display_time_hour=self.get_argument("start_display_time_morning")
        start_display_time = self.get_argument("start_display_time_year")+","+self.get_argument("start_display_time_month")+","+start_display_time_day+","+start_display_time_hour
        
        
        #data={'id':self.get_argument("id")}
        data={}
        data["start_display_time"] = str(int(time.mktime(time.strptime(start_display_time,"%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"]=self.get_argument("challenge")
        data["impede"]=self.get_argument("impede")
        data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")


        sql = "update task set title='"+data["title"]+"'"
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        sql=sql+",impede='"+self.get_argument("impede")+"' "
        sql=sql+",address='"+data["address"]+"'"
        print("地点post数据",self.get_arguments("address"))
        sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        print("sql语句:"+sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        print("result结果为:",result)
        
        res=requests.post(url1,data=data)
        print("http响应为:",res.content)
        self.write(res.content)
        
        
class selectHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_select_get方法了")

        #print("challenges:",dir(challenges))
      
        self.render("fileserver/templates/select.html"
        	
        	#,impedes=impedes
        	#,challenges=challenges
        	
        	)
        
    def post(self):
        print("进入fileserver_select_post方法了")
        #print("post数据:"+self.get_argument(status"))
        sql="select * from file where 1=1 "
        if self.get_argument("keyword","空值")!="空值":
            sql=sql+" and (name like '%"+self.get_argument("keyword")+"%')"
        if self.get_argument("address","空值")!="空值":
            sql=sql+" and (address like '%"+self.get_argument("address")+"%')"

        print("sql is:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        files=conn.cursor().execute(sql)
        result=conn.commit()


        print("files is:",files)
        #print("data is:",data)
        self.render("fileserver/templates/result.html"
        		,files=files)


class detailHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入filehouse_select_get方法了")
        sql="select * from file where id = "+self.get_argument("id")
        file=common.find("baigaopeng_fileserver",sql)
        self.render("fileserver/templates/detail.html"
        	,file=file
        	)
        
    def post(self):
        print("进入warehouse_select_post方法了")
        #print("post数据:"+self.get_argument(status"))
        sql="select * from file where 1=1 "
        if self.get_argument("keyword","空值")!="空值":
            sql=sql+" and (name like '%"+self.get_argument("keyword")+"%')"
        if self.get_argument("address","空值")!="空值":
            sql=sql+" and (address like '%"+self.get_argument("address")+"%')"
        print("sql is:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        files=conn.cursor().execute(sql)
        result=conn.commit()
        

        print("files is:",files)
        #print("data is:",data)
        self.render("fileserver/templates/result.html"
        		,files=files)

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_lists")
        #访问统计
        common.tongji("fileserver_lists")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            sql="select * from file"
            files=common.select("baigaopeng_fileserver",sql)
            print("files:",files)
            for vo in files:
                vo["liyonglv"]=int(vo["download_number"]/((time.time()-vo["ctime"])/86400)*10000)
            self.render("organization_admin/templates/File/lists.html"
                        ,files=files
                        )

