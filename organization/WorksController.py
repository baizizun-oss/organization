import tornado
import sqlite3
import urllib
import requests
import warnings
import os
import uuid
import cv2

warnings.filterwarnings('ignore')
import time
import myportal.common as common


class listsHandler(tornado.web.RequestHandler):
    def get(self):
        #print("获取到的开始时间",time.time())
        startTime= time.time()
        #self.clear_all_cookies()
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            #print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            works = common.select("organization","select * from works order by views desc")

            #print("works",works)
            #print("长度",len(works))
            for key in range(len(works)):
                #print("key",key)
                student = common.find("organization","select * from user where id = "+ str(works[key]["student_id"]))
                #print("student:",student)
                works[key]["student_name"] = student["nickname"]
                
                #评论部分                
                works_comments = common.select("organization","select works_comment.id,IFNULL(works_comment.comment, '暂无评论') as comment,user.nickname as student_name,works.id as works_id from works_comment,user,works where works_comment.student_id = user.id and works_id =" + str(works[key]["id"]) +" and works.id=works_comment.works_id")
                works[key]["comment"] = works_comments
                #print("评论",works_comments)
            #如果没有评论，就赋值为空
            for key in range(len(works)):
                if "comment" in works[key]:
                    continue
                else:
                    works[key]["comment"] = "" 
            #如果没有上传说明视频，就赋值为空
            for key in range(len(works)):
                if works[key]["works_introduction_video"]:
                    continue
                else:
                    works[key]["works_introduction_video"] = ""          
            #print("works:",works)

            # 分组处理（每5个一组）
            grouped_works = [works[i:i+5] for i in range(0, len(works), 5)]
            print("分组：",grouped_works)

            self.render(os.path.join(common.BASE_DIR,"organization","templates","Works","lists.html"),grouped_works=grouped_works,starttime= startTime,user_id = self.get_cookie("user_id"))

class detailHandler(tornado.web.RequestHandler):
    def get(self):
        #print("获取到的开始时间",time.time())
        startTime= time.time()
        #self.clear_all_cookies()
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            #print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            # 统计模块开始
            conn = sqlite3.connect(
                os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
            sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'design_list')"
            result = conn.cursor().execute(sql)
            conn.commit()
            conn.close()
            common.tongji("design_lists")
            # 统计模块结束

            works = common.select("organization","select * from works")
            #print("works",works)
            #print("长度",len(works))
            for key in range(len(works)):
                #print("key",key)
                student = common.find("organization","select * from user where id = "+ str(works[key]["student_id"]))
                #print("student:",student)
                works[key]["student_name"] = student["nickname"]
                
                #评论部分                
                works_comments = common.select("organization","select works_comment.id,IFNULL(works_comment.comment, '暂无评论') as comment,user.nickname as student_name,works.id as works_id from works_comment,user,works where works_comment.student_id = user.id and works_id =" + str(works[key]["id"]) +" and works.id=works_comment.works_id")
                works[key]["comment"] = works_comments
                #print("评论",works_comments)
            #如果没有评论，就赋值为空
            for key in range(len(works)):
                if "comment" in works[key]:
                    continue
                else:
                    works[key]["comment"] = "" 
            #如果没有上传说明视频，就赋值为空
            for key in range(len(works)):
                if works[key]["works_introduction_video"]:
                    continue
                else:
                    works[key]["works_introduction_video"] = ""          
            #print("works:",works)
            self.render("organization\\templates\\Works\\lists.html",works=works,starttime= startTime,user_id = self.get_cookie("user_id"))


class checkListHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(
            os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'task_index')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        sql = "select * from design where isChecked=0"
        designs = conn.cursor().execute(sql)
        conn.commit()
        self.render("organization\\templates\\Design\\lists.html",designs=designs)

class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        self.render(os.path.join(common.BASE_DIR,"organization","templates","Works","add.html"))

    def extract_video_cover(self,video_path, output_path):
        # 使用cv2.VideoCapture读取视频
        cap = cv2.VideoCapture(video_path)
        
        # 检查视频是否成功打开
        if not cap.isOpened():
            print("Error: Could not open video.")
            return
        
        # 读取视频的第一帧
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            return
        
        # 保存第一帧为图片
        cv2.imwrite(output_path, frame)
        print(f"Cover saved to {output_path}")
        
        # 释放VideoCapture对象
        cap.release()    

    def post(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            # 统计模块开始
            common.tongji("Works_add")
            # 统计模块结束
            #####数据检查开始########
            if self.get_argument("leifeng"):#如果填的有帮助人
                sql= "select * from user where nickname="+self.get_argument("leifeng")
                result = common.select("organization",sql)

                if result==None:#如不能比对出用户名说明填错了
                    self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("帮助人用户名不正确！");</script></body></html>')
            #####数据检查结束########
            # 上传文件的处理
            UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization","templates","Works","upload","")


            if self.request.files.get('works_file'):
                uploadFile = self.request.files['works_file'][0]
                # 生成新的文件名
                works_file = str(uuid.uuid4()) + os.path.splitext(uploadFile['filename'])[1]
                # 保存文件到服务器
                with open(os.path.join(UPLOAD_FILE_PATH, works_file), 'wb') as f:
                    f.write(uploadFile['body'])
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("请上传文件");</script></body></html>')   
       
            if self.request.files.get('works_introduction_file'):
                uploadFile = self.request.files['works_introduction_file'][0]
                # 生成新的文件名
                works_video_filename = str(uuid.uuid4()) + os.path.splitext(uploadFile['filename'])[1]
                video_path = os.path.join(UPLOAD_FILE_PATH, works_video_filename)
                print("video_path:",video_path)

                # 保存文件到服务器
                with open(video_path,'wb') as f:
                    f.write(uploadFile['body'])
                # 生成视频封面
                cover_path = os.path.join(UPLOAD_FILE_PATH, works_video_filename+".jpg")
                self.extract_video_cover(video_path, cover_path)
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");window.location.href = "http://bgp1984.eicp.net/organization/Works/lists";</script></body></html>')
            
            data = {}
            if self.get_argument("name"):
                data["works_name"] = self.get_argument("name")
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("请写清作品名");</script></body></html>')

            data["student_id"] = self.get_cookie("user_id")
            data["works_introduction_text"] = self.get_argument("works_introduction_text", "")
            data["works_introduction_video"] = works_video_filename
            data["works_file"] = works_file
            data["submit_time"] = str(int(time.time()))
            data["view_number"] = 0


            statements = []

            # 1. 插入作品
            sql1 = "INSERT INTO works(student_id,submit_time,works_name,works_introduction_text,works_introduction_video,views,works_file) VALUES (" + \
                data["student_id"] + "," + data["submit_time"] + ",'" + data["works_name"] + "','" + data["works_introduction_text"] + "','" + \
                data["works_introduction_video"] + "'," + str(data["view_number"]) + ",'" + data["works_file"] + "')"
            statements.append(sql1)

            # 2. 处理积分记录
            if self.get_argument("leifeng", None):
                # 查询雷锋用户
                sql2 = "SELECT * FROM user WHERE nickname=" + self.get_argument("leifeng")
                leifeng = common.select("organization", sql2)
                if leifeng and leifeng[0].get("id"):
                    now = str(int(time.time()))
                    statements.append(
                        "INSERT INTO user_score_history(user_id,score,ctime,score_source) VALUES (" +
                        str(leifeng[0]["id"]) + ",5," + now + ",'help_others')"
                    )
                    statements.append(
                        "INSERT INTO user_score_history(user_id,score,ctime,score_source) VALUES (" +
                        str(leifeng[0]["id"]) + ",-5," + now + ",'as_thank')"
                    )
            else:
                now = str(int(time.time()))
                statements.append(
                    "INSERT INTO user_score_history(user_id,score,ctime,score_source) VALUES (" +
                    data["student_id"] + ",10," + now + ",'works_add')"
                )

            # 原子执行所有语句（使用你新增的 executes 函数）
            try:
                common.executes("organization", statements)
                result = True  # 成功
            except Exception as e:
                # 可选：记录日志或返回错误
                print("事务失败:", e)
                raise  # 或者 return self.write({"error": "提交失败"})                       


class commentHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        self.render("organization/templates/Works/comment.html",works_id=self.get_argument("works_id"))
    def post(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            # 统计模块开始
            conn = sqlite3.connect(
                os.path.join(common.BASE_DIR,"organization","db","baigaopeng_myportal.db"))
            sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'design_list')"
            result = conn.cursor().execute(sql)
            conn.commit()
            conn.close()
            common.tongji("design_lists")
            # 统计模块结束

            data = {}
            if self.get_argument("comment"):
                data["comment"] = self.get_argument("comment")
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("请留下你的真知灼见！");</script></body></html>')

            data["works_id"] = self.get_argument("works_id")
            data["student_id"] = self.get_cookie("user_id")

            sql = "insert into works_comment(student_id,works_id,comment) values('" + data["student_id"] + "' \
                ,'" + data["works_id"] + "'\
                ,'"+ data["comment"] +"')"
            
            print("sql语句:" + sql)
            conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
            try:
                result = conn.cursor().execute(sql)
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("评论成功！");window.location.href = "http://192.168.100.251/organization/Works/lists";</script></body></html>')
            except:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("系统出错，请联系白老师！");</script></body></html>')
            print("result:", result)

            conn.commit()
            conn.close()


class detailHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        #浏览量+1
        sql = "update works set views=views+1 where id="+self.get_argument("works_id")
        try:
            result=common.execute("organization",sql)
        except:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("数据写入错误，请联系白老师！");</script></body></html>')
        print("result:", result)
        sql="select * from works where id=" + self.get_argument("works_id")
        work=common.find("organization",sql)
        sql="select * from works_comment join user on works_comment.student_id = user.id where works_comment.works_id=" + self.get_argument("works_id")
        comments=common.select("organization",sql)
        comments_number=len(comments)

        self.render(os.path.join(common.BASE_DIR,"organization","templates","Works","detail.html"),work=work,comments=comments,comments_number=comments_number)
    

class editHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        cursor=conn.cursor()
        sql="select * from design where id="+self.get_argument("id")
        result=cursor.execute(sql)
        design=cursor.fetchone()
        print(design)
        self.render("organization/templates/Design/edit.html"
                    , design=design
                    )

    def post(self):
        # print("进入task_edit_post方法了")

        data = {}
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')

        sql = "update design set evaluation='" + data["content"] + "'  where id=" + str(data["id"])
        # print("sql语句:"+sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        conn.cursor().execute(sql)
        result = conn.commit()
        conn.close()
        # print("result结果为:",result)
        self.write("评价成功！")

        # task的编辑模块


class delHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        sql = "delete from learn where id=" + self.get_argument("id")
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()


class doubleEditHandler(tornado.web.RequestHandler):
    def get(self):
        # print("进入task_doubleedit_get方法了")
        tasks = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from task where id=" + self.get_argument("id"))
        for vo in tasks:
            task = vo

        # print("tasks字符集：",tasks)
        # print("task字符集:",task)
        impedes = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from impede where status = 'abled'")
        challenges = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        # print("challenges:",dir(challenges))

        self.render("organization/Learn/templates/edit.html"

                    , task=task
                    , id=task[0]
                    , title=task[3]
                    , content=task[4].replace("&nbsp", " ").replace("<br>", "\n")
                    , status=task[5]
                    , address=task[6]
                    , challenge=task[11]
                    , photo1=task[10]
                    , photo2=task[11]
                    , photo3=task[12]
                    , type=task[7]
                    , impede=task[15]

                    , impedes=impedes
                    , challenges=challenges

                    )

    # 在这对python和php对于模拟客户端发起http请求的处理方法的不同做一个说明
    # php主要用作后端，一般不需要发起http请求，而是接收http请求。因此原生需要没有关于模拟浏览器发起http请求的功能是可以理解的。因此也就用到了curl这样的第三方类库
    # 而python是系统语言(或者用现在的说法是全栈语言)，可以需要对浏览器客户端进行开发，因此原生语言内置了模拟浏览器发起http请求的功能。就是client类。
    # 而它的使用和curl一样都是模拟了一个客户端类，用它的方法发起请求
    # @tornado.web.asynchronous
    def post(self):
        # print("post['address']:",self.get_arguments("address"))
        ##print("post数据:",self.get_argument())
        # url1   ="http://1.198.50.136:9000/organization/Learn/index.php/Home/Index/edit/id/"+self.get_argument("id")
        url1 = "http://192.168.43.1:8000/organization/Learn/Home/Index/edit?id=" + self.get_argument("id")
        url123 = "http://127.0.0.1:8000/organization/Learn/edit?id=" + self.get_argument("id")
        url_test = "http://192.168.43.1:8080/organization/Learn/index.php?m=Home&c=index&a=doubleedit&id=" + self.get_argument("id")

        # data={"id":self.get_arguments("id")}
        if self.get_argument("start_display_time_first_half") == time.strftime("%d"):
            start_display_time_day = self.get_argument("start_display_time_second_half")
        else:
            start_display_time_day = self.get_argument("start_display_time_first_half")
        if self.get_argument("start_display_time_morning") == time.strftime("%H"):
            start_display_time_hour = self.get_argument("start_display_time_afternoon")
        else:
            start_display_time_hour = self.get_argument("start_display_time_morning")
        start_display_time = self.get_argument("start_display_time_year") + "," + self.get_argument(
            "start_display_time_month") + "," + start_display_time_day + "," + start_display_time_hour

        # data={'id':self.get_argument("id")}
        data = {}
        data["start_display_time"] = str(int(time.mktime(time.strptime(start_display_time, "%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"] = self.get_argument("challenge")
        data["impede"] = self.get_argument("impede")
        data["address"] = ",".join(self.get_arguments("address[]"))
        data["status"] = self.get_argument("status")

        sql = "update task set title='" + data["title"] + "'"
        sql = sql + ",content='" + data["content"].replace(" ", "&nbsp").replace("\n", "<br>").replace("'",
                                                                                                       "&apos") + "'"
        sql = sql + ",start_display_time=" + data["start_display_time"]
        sql = sql + ",status = '" + self.get_argument("status") + "'"
        sql = sql + ",impede='" + self.get_argument("impede") + "' "
        sql = sql + ",address='" + data["address"] + "'"
        # print("地点post数据",self.get_arguments("address"))
        sql = sql + ",challenge='" + self.get_argument("challenge") + "'"
        sql = sql + " where id=" + str(data["id"])
        # print("sql语句:"+sql)
        conn = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        conn.cursor().execute(sql)
        result = conn.commit()
        conn.close()
        # print("result结果为:",result)

        res = requests.post(url1, data=data)
        ###print("http响应为:",res.content)
        self.write(res.content)


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        # print("进入task_select_get方法了")

        impedes = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from impede where status = 'abled'")
        challenges = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        # print("challenges:",dir(challenges))

        self.render("organization/Learn/templates/select.html"

                    , impedes=impedes
                    , challenges=challenges

                    )

    def post(self):
        # print("进入task_select_post方法了")
        # print("post数据:"+self.get_argument(status"))
        sql = "select * from task where 1=1 "
        if self.get_argument("status", "空值") != "空值":
            sql = sql + " and (status like '%" + self.get_argument("status") + "%')"
        if self.get_argument("impede", "空值") != "空值":
            sql = sql + " and (impede like '%" + self.get_argument("impede") + "%')"
        if len(self.get_arguments("address[]", "空值")) > 0:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[0] + "%') "
        if len(self.get_arguments("address[]", "空值")) > 1:
            sql = sql + " and (address like '%" + self.get_arguments("address[]")[1] + "%')"
        if self.get_argument("keyword", "空值") != "空值":
            sql = sql + " and (title like '%" + self.get_argument("keyword") + "%' or \
        	 content like '%" + self.get_argument("keyword") + "%' or \
        	 id like '%" + self.get_argument("keyword") + "%' \
        	)"
        if self.get_argument("keyword2", "nullvalue") != "nullvalue":
            sql = sql + " and (title like '%" + self.get_argument("keyword2") + "%' or \
        		content like '%" + self.get_argument("keyword2") + "%' or \
        		id like '%" + self.get_argument("keyword2") + "%' \
        		)"

        if len(self.get_arguments("type[]", "nullvalue")) > 0:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[0] + "%'")
        if len(self.get_arguments("type[]", "nullvalue")) > 1:
            sql = sql + (" and type like '%" + self.get_arguments("type[]")[1] + "%'")
        if self.get_argument("challenge", "nullvalue") != "nullvalue":
            sql = sql + (" and challenge like '%" + self.get_argument("challenge") + "%'")
        sql = sql + " order by id asc"
        # print("sql is:",sql)
        conn = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        tasks = conn.cursor().execute(sql)
        result = conn.commit()

        data = ({"id": 1, "title": "first", "content": "first_content"}
                , {"id": 2, "title": "second", "content": "second_content"}
                )
        #	for name,value in taskset.items():
        # print('%s=%s'%(name,value))
        '''

        for row in tasks:
            data[0]["id"]=row[0]
            data[0]["title"]=row[1]
            data[0]["content"]=row[2]
            #print("tasks集合为 is:",row[0])

        for row in tasks:
            data[0]["id"]=row[0]
            data[0]["title"]=row[1]
            data[0]["content"]=row[2]
            #print("tasks集合为 is:",row[0])
        '''

        # print("tasks is:",tasks)
        ##print#print("data is:",data)
        self.render("organization/Learn/templates/result.html"
                    , tasks=tasks)
        #	       #conn.
        '''
("select * from task where (status like '%".$_POST["status"]."%') AND (address like '%".$_POST['address'][0]."%') AND (title like '%".$_POST['keyword']."%' OR content like '%".$_POST['keyword']."%') AND (type like '%".$_POST["type"][0]."%') AND (challenge like '%".$_POST["challenge"]."%') order by id asc");
            //其中关键词使用mysql_escape_string()函数对输入字符串进行过滤(其实就是将那么mysql的敏感词可以透过mysql传到mysql的字段中去)
        		  	 	AND (type like '%".$_POST["type"][0]."%') 
        		  	 	and (type like '%".$_POST["type"][1]."%')
        	 AND (challenge like '%".$_POST["challenge"]."%')
        	  order by id asc");
            $this->assign('note',$note);
            $code_end_time=time();
            $duration=$code_end_time-$code_start_time;
            dump("此次查询花费".$duration."ms");
            $this->mydisplay("index");
        '''
# 点击视频处理
class IncrementViewHandler(tornado.web.RequestHandler):
    async def get(self):
        # 更新数据库浏览数
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        cursor = conn.cursor()
        cursor.execute("UPDATE works SET view_number = view_number + 1 WHERE id = ?", self.get_argument("works_id"))
        conn.commit()
        conn.close()
        
        # 获取实际视频路径（假设 vo['works_introduction_video'] 是文件名）
        video_path = os.path.join("organization/templates/Works/upload/", vo['works_introduction_video'])
        
        # 返回视频文件
        with open(video_path, "rb") as f:
            self.set_header("Content-Type", "video/mp4")
            self.write(f.read())
        self.finish()