import tornado
import sqlite3
import urllib
import requests
import warnings

warnings.filterwarnings('ignore')
import time
import myportal.common as common


class listsHandler(tornado.web.RequestHandler):
    def get(self):
        #self.clear_all_cookies()
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")
            #self.render("sangao/templates/Index/login.html")
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

            conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
            sql = "select * from design where isChecked=1"
            designs = conn.cursor().execute(sql)
            conn.commit()
            self.render("sangao\\templates\\Design\\lists.html",designs=designs)

class checkListHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(
            "D:\\projects3\\db\\baigaopeng_myportal.db")
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'task_index')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        sql = "select * from design where isChecked=0"
        designs = conn.cursor().execute(sql)
        conn.commit()
        self.render("sangao\\templates\\Design\\lists.html",designs=designs)

class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        self.render("sangao/templates/Design/add.html")
    def post(self):
        # 上传文件的处理
        UPLOAD_FILE_PATH = 'sangao\\templates\\Design\\upload\\'
        # username = self.get_argument('username', 'anonymous')
        if self.request.files.get('file', None):
            uploadFile = self.request.files['file'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])

        self.write("上传成功")
        data = {}

        data["filepath"] =  filename
        data["name"] = self.get_argument("name")

        sql = "insert into design(name,path,isChecked) values('" + data[
            "name"] + "' \
        	,'" + data["filepath"] + "',0)"
        print("sql语句:" + sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        result = conn.cursor().execute(sql)
        print("result:", result)

        conn.commit()
        conn.close()


class editHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor=conn.cursor()
        sql="select * from design where id="+self.get_argument("id")
        result=cursor.execute(sql)
        design=cursor.fetchone()
        print(design)
        self.render("sangao/templates/Design/edit.html"
                    , design=design
                    )

    def post(self):
        # print("进入task_edit_post方法了")

        data = {}
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')

        sql = "update design set evaluation='" + data["content"] + "'  where id=" + str(data["id"])
        # print("sql语句:"+sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
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
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
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

        self.render("sangao/Learn/templates/edit.html"

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
        # url1   ="http://1.198.50.136:9000/sangao/Learn/index.php/Home/Index/edit/id/"+self.get_argument("id")
        url1 = "http://192.168.43.1:8000/sangao/Learn/Home/Index/edit?id=" + self.get_argument("id")
        url123 = "http://127.0.0.1:8000/sangao/Learn/edit?id=" + self.get_argument("id")
        url_test = "http://192.168.43.1:8080/sangao/Learn/index.php?m=Home&c=index&a=doubleedit&id=" + self.get_argument("id")

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

        self.render("sangao/Learn/templates/select.html"

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
        self.render("sangao/Learn/templates/result.html"
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
