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
        # 统计模块开始
        conn = sqlite3.connect(
            "D:\\projects3\\db\\baigaopeng_myportal.db")
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'exam_lists')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        sql = "select * from exam_paper"
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        print(exam_papers)
        self.render("sangao\\templates\\Exam\\exam_paper_lists.html",exam_papers=exam_papers)


class examPaperAddHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        common.tongji("exam_paper_add")
        self.render("sangao/templates/Exam/exam_paper_add.html")
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["ctime"]=str(int(time.time()))
        data["one"] = ""
        data["two"] = ""
        data["three"]=""
        data["four"]=""
        data["five"]=""
        data["six"]=""
        data["seven"]=""
        data["eight"]=""
        data["nine"]=""
        data["ten"]=""
        data["eleven"]=""
        data["twelve"]=""
        data["thirteen"]=""
        data["fourteen"]=""
        data["fifteen"]=""
        data["sixteen"]=""
        data["seventeen"]=""
        data["eighteen"]=""
        data["nineteen"]=""
        data["twenty"]=""
        data["twentyone"]=""
        data["twentytwo"]=""
        UPLOAD_FILE_PATH = 'sangao\\templates\\Exam\\upload\\'
        if self.request.files.get('one', None):
            uploadFile = self.request.files['one'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["one"]=filename
        if self.request.files.get('two', None):
            uploadFile = self.request.files['two'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["two"]=filename
        if self.request.files.get('three', None):
            uploadFile = self.request.files['three'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["three"]=filename
        if self.request.files.get('four', None):
            uploadFile = self.request.files['four'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["four"]=filename
        if self.request.files.get('five', None):
            uploadFile = self.request.files['five'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["five"]=filename
        if self.request.files.get('six', None):
            uploadFile = self.request.files['six'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["six"]=filename
        if self.request.files.get('seven', None):
            uploadFile = self.request.files['seven'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["seven"]=filename
        if self.request.files.get('eight', None):
            uploadFile = self.request.files['eight'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["eight"]=filename
        if self.request.files.get('nine', None):
            uploadFile = self.request.files['nine'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["nine"]=filename
        if self.request.files.get('ten', None):
            uploadFile = self.request.files['ten'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["ten"] = filename
        if self.request.files.get('eleven', None):
            uploadFile = self.request.files['eleven'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["eleven"] = filename
        if self.request.files.get('twelve', None):
            uploadFile = self.request.files['twelve'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twelve"] = filename
        if self.request.files.get('thirteen', None):
            uploadFile = self.request.files['thirteen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["thirteen"] = filename
        if self.request.files.get('fourteen', None):
            uploadFile = self.request.files['fourteen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["fourteen"] = filename
        if self.request.files.get('fifteen', None):
            uploadFile = self.request.files['fifteen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["fifteen"] = filename
        if self.request.files.get('sixteen', None):
            uploadFile = self.request.files['sixteen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["sixteen"] = filename
        if self.request.files.get('seventeen', None):
            uploadFile = self.request.files['seventeen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["seventeen"] = filename
        if self.request.files.get('eighteen', None):
            uploadFile = self.request.files['eighteen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["eighteen"] = filename
        if self.request.files.get('nineteen', None):
            uploadFile = self.request.files['nineteen'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["nineteen"] = filename
        if self.request.files.get('twenty', None):
            uploadFile = self.request.files['twenty'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twenty"] = filename
        if self.request.files.get('tnentyone', None):
            uploadFile = self.request.files['tnentyone'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["tnentyone"] = filename
        if self.request.files.get('twentytwo', None):
            uploadFile = self.request.files['twentytwo'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twentytwo"] = filename


        print(data)
        sql = "insert into exam_paper(title,ctime,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo) values('"+data["title"] +"',"+data["ctime"]+\
        ",'"+data["one"]+\
        "','"+data["two"]+\
        "','"+data["three"]+\
        "','"+data["four"]+\
        "','"+data["five"]+\
        "','"+data["six"]+\
        "','"+data["seven"]+\
        "','"+data["eight"]+\
        "','"+data["nine"]+\
        "','"+data["ten"]+\
        "','"+data["eleven"]+\
        "','"+data["twelve"]+\
        "','"+data["thirteen"]+\
        "','"+data["fourteen"]+\
        "','"+data["fifteen"]+\
        "','"+data["sixteen"]+\
        "','"+data["seventeen"]+\
        "','"+data["eighteen"]+\
        "','"+data["nineteen"]+\
        "','"+data["twenty"]+\
        "','"+data["twentyone"]+\
        "','"+data["twentytwo"]+\
        "')"
        print("sql语句:" + sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        result = conn.cursor().execute(sql)
        print("result:", result)

        conn.commit()
        conn.close()
        self.write("添加成功")

class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("暂无权限！请联系管理员!")

        
class editHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor=conn.cursor()
        sql="select * from design where id="+self.get_argument("id")
        result=cursor.execute(sql)
        design=cursor.fetchall()
        print(design)
        self.render("sangao/templates/Design/edit.html"
                    , design=design
                    )

    def post(self):
        # print("进入task_edit_post方法了")

        data = {}
        data["start_display_time"] = self.get_argument("start_display_time")
        # data["start_display_time"] = str(int(time.mktime(time.strptime(self.get_argument("start_display_time"),"%Y,%m,%d,%H"))))
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
        sql = sql + ",address='" + ",".join(self.get_arguments("address")) + "'"
        # print("地点post数据",self.get_arguments("address"))
        sql = sql + ",challenge='" + self.get_argument("challenge") + "'"
        sql = sql + " where id=" + str(data["id"])
        # print("sql语句:"+sql)
        conn = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        conn.cursor().execute(sql)
        result = conn.commit()
        conn.close()
        # print("result结果为:",result)
        self.write("")

        # task的编辑模块


class examPaperDelHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        common.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()



class handinHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入交卷模块")
        common.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
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
class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #访问统计
        common.tongji("exam_index")

        #代码开始
        sql="select * from exam_paper where id="+self.get_argument("id")
        exam_paper=common.find("sangao",sql)
        print(exam_paper)
        self.render("sangao\\templates\\Exam\\index.html",exam_paper=exam_paper)
    def post(self):
        data={}
        data["ctime"]= str(int(time.time()))
        data["student_name"]=self.get_argument("name","none")
        data["one"]=self.get_argument("one","none")
        data["two"]=self.get_argument("two","none")
        data["three"]=self.get_argument("three","none")
        data["four"]=self.get_argument("four","none")
        data["five"]=self.get_argument("five","none")
        data["six"]=self.get_argument("six","none")
        data["seven"]=self.get_argument("seven","none")
        data["eight"]=self.get_argument("eight","none")
        data["nine"]=self.get_argument("nine","none")
        data["ten"]=self.get_argument("ten","none")
        data["eleven"]=self.get_argument("eleven","none")
        data["twelve"]=self.get_argument("twelve","none")
        data["thirteen"]=self.get_argument("thirteen","none")
        data["fourteen"]=self.get_argument("fourteen","none")
        data["fifteen"]=self.get_argument("fifteen","none")
        data["sixteen"]=self.get_argument("sixteen","none")
        data["seventeen"]=self.get_argument("seventeen","none")
        data["eighteen"]=self.get_argument("eighteen","none")
        data["nineteen"]=self.get_argument("nineteen","none")
        data["twenty"]=self.get_argument("twenty","none")
        data["twentyone"]=self.get_argument("twentyone","none")
        data["twentytwo"]=self.get_argument("twentytwo","none")
        print(data)
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        self.write("提交完成！")

class errorRankingHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("sangao/templates/Exam/error_ranking_select.html",exam_papers=exam_papers)


class singleChoiceAddHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        sql="insert into single_choice_question()"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("sangao/templates/Question/single_choice_add.html",exam_papers=exam_papers)




class selectHandler(tornado.web.RequestHandler):
    def get(self):
        # print("进入task_select_get方法了")

        impedes = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from impede where status = 'abled'")
        challenges = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        # print("challenges:",dir(challenges))

        self.render("sangao/templates/Question/select.html"

                    , impedes=impedes
                    , challenges=challenges

                    )

    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        print("post_data:",post_data)
        data={}
        data["module"]=self.get_argument("module")
        single_choice_questions={}
        true_false_questions={}
        operation_questions={}
        if self.get_argument("type")=="single_choice":
            sql="select * from single_choice_question where module='"+data["module"]+"'"
            single_choice_questions=common.select("sangao",sql)
        if self.get_argument("type")=="true-false":
            sql="select * from true-false_question"
            true_false_questions=common.select("sangao",sql)
        if self.get_argument("type")=="operation":
            sql="select * from operation_question"
            operation_questions=common.select("sangao",sql) 
        print("结果集single_choice_questions",single_choice_questions)       
        print("结果集true_false_questions",true_false_questions)
        print("结果集operation_questions",operation_questions)

        self.render("D:\\projects3\\sangao\\templates\\Question\\result.html"
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,single_choice_questions=single_choice_questions)

