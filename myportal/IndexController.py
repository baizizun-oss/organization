#-*-coding:utf8;-*-
#qpy:console


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




class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_Index_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render("myportal/templates/Index/index.html")
    def on_response(self,response):
        body= json.loads(response.body)
        #print("response内容为:",body)
        self.finish
        
class quickSelectHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'quick_select')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        #self.render("myportal/templates/Index/quick_select.html")        
        #print("进入myportal_index_quickselect_get方法了")
        #tasks=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from task where id="+self.get_argument("id"))
        #for vo in tasks:
            #task=vo
            
        #print("tasks字符集：",tasks)
        #print("task字符集:",task)
        impedes=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from impede where status = 'abled'")
        #for vo in impedes:
            #print("impedes[0]:",vo[0])
        challenges=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        #for vi in challenges:
            #print("challenges[0]:",vi[0])
        self.render("myportal/templates/Index/quick_select.html"
        	,impedes=impedes
        	,challenges=challenges
        	)
    
    def post(self):
        print("进入myportal_index_quick_select_post")
        '''
     		//用三个and并列质疑name中含有三个关键词的记录
    		//每个关键词的查询范围为标题和内容
        '''
        sql = "select * from task where 1=1 "
        
        if self.get_argument("status","空值")!="空值":
            sql=sql+" and (status like '%"+self.get_argument("status")+"%')"
        if self.get_argument("impede","空值")!="空值":
            sql=sql+" and (impede like '%"+self.get_argument("impede")+"%')"
        if len(self.get_arguments("address[]","空值"))>0:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[0]+"%') "
        if len(self.get_arguments("address[]","空值"))>1:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[1]+"%')"
        if self.get_argument("keyword1","空值")!="空值":
            sql=sql+" and (title like '%"+self.get_argument("keyword1")+"%' or \
        	 content like '%"+self.get_argument("keyword1")+"%' or \
        	 id like '%"+self.get_argument("keyword1")+"%' \
        	)"
        if self.get_argument("keyword2","nullvalue")!="nullvalue":
            sql=sql+" and (title like '%"+self.get_argument("keyword2")+"%' or \
        		content like '%"+self.get_argument("keyword2")+"%' or \
        		id like '%"+self.get_argument("keyword2")+"%' \
        		)"
        if self.get_argument("keyword3","nullvalue")!="nullvalue":
            sql=sql+" and (title like '%"+self.get_argument("keyword3")+"%' or \
        		content like '%"+self.get_argument("keyword3")+"%' or \
        		id like '%"+self.get_argument("keyword3")+"%' \
        		)"        		
        if len(self.get_arguments("type[]","nullvalue"))>0:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[0]+"%'")
        if len(self.get_arguments("type[]","nullvalue"))>1:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[1]+"%'")
        if self.get_argument("challenge","nullvalue")!="nullvalue":
            sql=sql+(" and challenge like '%"+self.get_argument("challenge")+"%'")
        sql_problem=sql+" order by id asc"
        sql_task=sql+" and start_display_time<"+str(int(time.time()))+" order by id asc "

        problems=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute(sql+" order by id asc")
        tasks   =sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute(sql_task)
        problem_develops=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute(sql_problem)
        task_develops   =sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute(sql_task)
        problem_develop_tests=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute(sql_problem)
        task_develop_tests   =sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute(sql_task)
        self.render("myportal/templates/Index/quick_select_result.html"
        		,problems=problems
        		,tasks=tasks
        		,problem_develops=problem_develops
        		,task_develops=task_develops
        		,problem_develop_tests=problem_develop_tests
        		,task_develop_tests=task_develop_tests
        		)

class clickSelectHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'click_select')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        #print("now is accessing myportal_index_click_select_get")
        self.render("myportal/templates/Index/click_select.html")
    def post(self):
        #print("now is accessing myporta_index_click_select_post")
        data={}
        #start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        #data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        #end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        #data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        #data["start_time"]=self.get_argument("start_time")
        #data["end_time"]=self.get_argument("end_time")
        
        
        #sql="insert into holiday(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        sql="select count(*) as fangwen_num,click_action from click group by click_action"
        #print("sql sentence:",sql)
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        cursor=conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():#从fetchall中读取操作 print(row)
            print("result:",row)
            #self.write(row)
        conn.commit()
        conn.close()
        #self.write("添加成功！")
        #self.write(result)
   
        	        
     ###################
     ##
     # 一键执行运行秩序
     #
     ###################
class operationOrderHandler(tornado.web.RequestHandler):
    def get(self):
      conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
      sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'operation_order')"
      result=conn.cursor().execute(sql)
      conn.commit()
      conn.close()
      now_time="上班期间"#默认为上班期间
      now_class_time="上课期间"
      holidays = sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from holiday")
      class_times = sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from class_time")

      #print("holidays字符集:",holidays)
      for vo in holidays:
          if (time.time()<vo[2] and time.time()>vo[1]):
              now_time="下班期间"

      for vo in class_times:
          if (time.time()<vo[2] and time.time()>vo[1]):
              now_time="上课期间"
            
      #print("上班期间或者下班期间:",now_time)

      #通过附近wifi获取到的当前地点
      address=common.getAddress()
      print("address:",address)
      #通过LBS(基站模式)获取的当前地点
      lbs_longitude=self.get_argument("longitude","")
      lbs_latitude =self.get_argument("latitude","")
      #获取当前手机的名称
      currentPhone=common.getPhoneName()
      #写入文件保存
      f=open(os.path.join("myportal","position.txt"),'a')
      f.write(time.strftime("%H")+":"+time.strftime("%M")+"wifi地点:"+address+"lbs_latitude:"+lbs_latitude+"lbs_longitude:"+lbs_longitude+"当前手机:"+currentPhone+"\r\n")
      #通过lbs获取到当前地址
      address_lbs=common.getLbsAddress(lbs_latitude,lbs_longitude)
      #if address_lbs != address:
          #address=""


    		#《问题笔记系统》中优先级为&^￥^,状态为”未处理“ --上课时间
      problem_12 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+" and title like '%&^¥^%'")
      task_12=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%&^¥^%' ")
      #problem_develop10=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_12=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")  
      #problem_developtest_10=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_test_12=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      #'试验机正被占用','必须在"+address+"处理'
      problem_13=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_13=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ") 	
      test="select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' "
      #print("sql语句:"+test)
      #problem_develop11=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_13=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      #problem_developtest_11=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_test_13=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")

    		#《问题笔记系统》中优先级为&^￥^,状态为”未处理“
      problem_10 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+" and title like '%&^¥^%'")
      task_10=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%&^¥^%' ")
      #problem_develop10=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_10=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")  
      #problem_developtest_10=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_test_10=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      #'试验机正被占用','必须在"+address+"处理'
      problem_11=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_11=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ") 	
      test="select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' "
      #print("sql语句:"+test)
      #problem_develop11=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_11=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      #problem_developtest_11=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")
      task_develop_test_11=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^¥^%' ")


      problem_14 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%'")
      task_14=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%&^%' ")
      task_develop_14=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      task_develop_test_14=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
              

      
      problem_1 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%'")
      task_1=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%&^%' ")
      #problem_develop1=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      task_develop_1=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      #problem_developtest_1=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")         
      task_develop_test_1=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      
      problem_15=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      task_15=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")	
      task_develop_15=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      task_develop_test_15=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
   

      problem_2=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      task_2=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")	
      task_develop_2=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
      task_develop_test_2=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%&^%' ")
     
      problem_16=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")
      task_16=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")	
      task_develop_16=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")
      task_develop_test_16=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")
      

      problem_3=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")
      task_3=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")	
      task_develop_3=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")
      task_develop_test_3=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede='需要外出' and start_display_time<"+str(int(time.time()))+" and title like '%&^%' ")
      
      problem_17 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%'")
      task_17=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%¥^%' ")
      task_develop_17=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")  
      task_develop_test_17=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      
      
      problem_4 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%'")
      task_4=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%¥^%' ")
      task_develop_4=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")  
      task_develop_test_4=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      
      problem_18=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      task_18=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ") 	
      task_develop_18=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      task_develop_test_18=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      

      problem_5=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      task_5=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ") 	
      task_develop_5=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      task_develop_test_5=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%¥^%' ")
      
      problem_19 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%%'")
      task_19=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%%' ")
      task_develop_19=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")  
      task_develop_test_19=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")
    

      problem_7 = sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%%'")
      task_7=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and status='未处理' and start_display_time< "+str(int(time.time()))+"  and title like '%%' ")
      task_develop_7=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")  
      task_develop_test_7=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='未处理' and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")

      problem_20=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")
      task_20=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ") 	
      task_develop_20=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")
      task_develop_test_20=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_class_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")

      problem_8=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute("select * from task where status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")
      task_8=sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ") 	
      task_develop_8=sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")
      task_develop_test_8=sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute("select * from task where title like '%"+now_time+"%' and  status='遇阻' and impede in ('缺少实体资源','需要自己还不懂的知识','需要有序进行试验','需要外出','试验机正被占用','必须在"+address+"处理') and start_display_time<"+str(int(time.time()))+"  and title like '%%' ")
      


      self.render("myportal/templates/Index/operation_order_result.html"
      	,problem_12=problem_12
      	,task_12=task_12
      	,task_develop_12=task_develop_12
      	,task_develop_test_12=task_develop_test_12
      	,problem_13=problem_13
      	,task_13=task_13
      	,task_develop_13=task_develop_13
      	,task_develop_test_13=task_develop_test_13 
            
      	,problem_14=problem_14
      	,task_14=task_14
      	,task_develop_14=task_develop_14
      	,task_develop_test_14=task_develop_test_14
          
      	,problem_15=problem_15
      	,task_15=task_15
      	,task_develop_15=task_develop_15
      	,task_develop_test_15=task_develop_test_15
          
      	,problem_16=problem_16
      	,task_16=task_16
      	,task_develop_16=task_develop_16
      	,task_develop_test_16=task_develop_test_16

      	,problem_17=problem_17
      	,task_17=task_17
      	,task_develop_17=task_develop_17
      	,task_develop_test_17=task_develop_test_17

      	,problem_18=problem_18
      	,task_18=task_18
      	,task_develop_18=task_develop_18
      	,task_develop_test_18=task_develop_test_18

      	,problem_19=problem_19
      	,task_19=task_19
      	,task_develop_19=task_develop_19
      	,task_develop_test_19=task_develop_test_19

      	,problem_20=problem_20
      	,task_20=task_20
      	,task_develop_20=task_develop_20
      	,task_develop_test_20=task_develop_test_20

      	,problem_10=problem_10
      	,task_10=task_10
      	,task_develop_10=task_develop_10
      	,task_develop_test_10=task_develop_test_10
      	,problem_11=problem_11
      	,task_11=task_11
      	,task_develop_11=task_develop_11
      	,task_develop_test_11=task_develop_test_11
          
      	,problem_1=problem_1
      	,task_1=task_1
      	,task_develop_1=task_develop_1
      	,task_develop_test_1=task_develop_test_1
          
      	,problem_2=problem_2
      	,task_2=task_2
      	,task_develop_2=task_develop_2
      	,task_develop_test_2=task_develop_test_2
      	,problem_3=problem_3
      	,task_3=task_3
      	,task_develop_3=task_develop_3
      	,task_develop_test_3=task_develop_test_3      	
      	,problem_4=problem_4
      	,task_4=task_4
      	,task_develop_4=task_develop_4
      	,task_develop_test_4=task_develop_test_4
      	,problem_5=problem_5
      	,task_5=task_5
      	,task_develop_5=task_develop_5
      	,task_develop_test_5=task_develop_test_5  	
      	,problem_7=problem_7
      	,task_7=task_7
      	,task_develop_7=task_develop_7
      	,task_develop_test_7=task_develop_test_7
      	,problem_8=problem_8
      	,task_8=task_8
      	,task_develop_8=task_develop_8
      	,task_develop_test_8=task_develop_test_8     	

      	)
        
class allSelectHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'quick_select')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束

        impedes=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from impede where status = 'abled'")
        challenges=sqlite3.connect(os.path.join("db","baigaopeng_myportal.db")).cursor().execute("select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        self.render("myportal/templates/Index/all_select.html"
        	,impedes=impedes
        	,challenges=challenges
        	)
    
    def post(self):
        print("进入myportal_index_quick_select_post")
        '''
     		//用三个and并列质疑name中含有三个关键词的记录
    		//每个关键词的查询范围为标题和内容
        '''
        sql = "select * from task where 1=1 "
        
        if self.get_argument("status","空值")!="空值":
            sql=sql+" and (status like '%"+self.get_argument("status")+"%')"
        if self.get_argument("impede","空值")!="空值":
            sql=sql+" and (impede like '%"+self.get_argument("impede")+"%')"
        if len(self.get_arguments("address[]","空值"))>0:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[0]+"%') "
        if len(self.get_arguments("address[]","空值"))>1:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[1]+"%')"
        if self.get_argument("keyword1","空值")!="空值":
            sql=sql+" and (title like '%"+self.get_argument("keyword1")+"%' or \
        	 content like '%"+self.get_argument("keyword1")+"%' or \
        	 id like '%"+self.get_argument("keyword1")+"%' \
        	)"
        if self.get_argument("keyword2","nullvalue")!="nullvalue":
            sql=sql+" and (title like '%"+self.get_argument("keyword2")+"%' or \
        		content like '%"+self.get_argument("keyword2")+"%' or \
        		id like '%"+self.get_argument("keyword2")+"%' \
        		)"
        if self.get_argument("keyword3","nullvalue")!="nullvalue":
            sql=sql+" and (title like '%"+self.get_argument("keyword3")+"%' or \
        		content like '%"+self.get_argument("keyword3")+"%' or \
        		id like '%"+self.get_argument("keyword3")+"%' \
        		)"        		
        if len(self.get_arguments("type[]","nullvalue"))>0:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[0]+"%'")
        if len(self.get_arguments("type[]","nullvalue"))>1:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[1]+"%'")
        if self.get_argument("challenge","nullvalue")!="nullvalue":
            sql=sql+(" and challenge like '%"+self.get_argument("challenge")+"%'")
        sql_problem=sql+" order by id asc"
        sql_task=sql+" order by id asc "

        problems=sqlite3.connect(os.path.join("db","baigaopeng_problem.db")).cursor().execute(sql+" order by id asc")
        tasks   =sqlite3.connect(os.path.join("db","baigaopeng_task.db")).cursor().execute(sql_task)
        problem_develops=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop.db").cursor().execute(sql_problem)
        task_develops   =sqlite3.connect(os.path.join("db","baigaopeng_task_develop.db")).cursor().execute(sql_task)
        problem_develop_tests=sqlite3.connect("/storage/emulated/0/qpython/projects3/db/baigaopeng_problem_develop_test.db").cursor().execute(sql_problem)
        task_develop_tests   =sqlite3.connect(os.path.join("db","baigaopeng_task_develop_test.db")).cursor().execute(sql_task)
        self.render("myportal/templates/Index/all_select_result.html"
        		,problems=problems
        		,tasks=tasks
        		,problem_develops=problem_develops
        		,task_develops=task_develops
        		,problem_develop_tests=problem_develop_tests
        		,task_develop_tests=task_develop_tests
        		)
