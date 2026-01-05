import tornado
import sqlite3
import urllib
import requests
import warnings
import os
warnings.filterwarnings('ignore')
import time
import myportal.common as common




class listsHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        common.tongji("question_lists")
        # 统计模块结束
        sql="select * from question"
        questions=common.select("organization",sql)
     
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","lists.html"),questions=questions)


class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","add.html"))
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["type"]=self.get_argument("type")
        data["difficult"]=self.get_argument("difficult")
        data["notice"]=self.get_argument("notice")
        data["input_format"]=self.get_argument("input_format")
        data["output_format"]=self.get_argument("output_format")


        #取出当前要添加的id(要给文件名使用)
        sql="select * from question order by id desc limit 1"
        question= common.find("organization",sql)

        #测试用例输入的处理
        UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Question","test_data_input","")
        if self.request.files.get('test_data_input', None):
            uploadFile = self.request.files['test_data_input'][0]
            filename = uploadFile['filename']
            timestamp = int(time.time())
            data["test_data_input"] = UPLOAD_FILE_PATH  + str(question["id"]+1)+filename
            with open(data["test_data_input"],"wb") as file:
                file.write(uploadFile['body'])

        else:
            data["test_data_input"]=""

        #测试用例输出的处理
        UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Question","test_data_output","")
        if self.request.files.get('test_data_output', None):
            uploadFile = self.request.files['test_data_output'][0]
            filename = uploadFile['filename']
            timestamp = int(time.time())
            data["test_data_output"] = UPLOAD_FILE_PATH  + str(question["id"]+1)+filename
            #save_path = "File/upload/"+str(timestamp)+filename
            with open(data["test_data_output"],"wb") as file:
                file.write(uploadFile['body'])
        else:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("没有添加测试用例！");</script></body></html>')

        sql="insert into question(id,title,type,difficult,test_data_input,test_data_output,notice,input_format,output_format) values("+str(question["id"]+1)+",'"+data["title"]+"','"+data["type"]+"','"+data["difficult"]+"','"+data["test_data_input"]+"','"+data["test_data_output"]+"','"+data["notice"]+"','"+data["input_format"]+"','"+data["output_format"]+"')"
        result=common.execute("organization",sql)
        if result:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");</script></body></html>')
        else:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加失败！");</script></body></html>')
        
class detailHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from question where id="+self.get_argument("id")
        question=common.find("organization",sql)
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","detail.html"),question=question)


class editHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_argument("question_type")=="single_choice":
            sql="select * from single_choice_question where id="+self.get_argument("id")
            single_choice_question=common.find("organization",sql)
            print("single_choice")
            self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","single_choice_edit.html"),single_choice_question=single_choice_question)
        if self.get_argument("question_type")=="tf":
            sql="select * from tf_question where id="+self.get_argument("id")
            tf_question=common.find("organization",sql)
            print("tf")
            self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","tf_edit.html"),tf_question=tf_question)
        if self.get_argument("question_type")=="operation":
            sql="select * from operation where id="+self.get_argument("id")
            operation_question=common.find("organization",sql)
            print("operation")
            self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","operation_edit.html"),operation_question=operation_question)
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
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
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
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        result = conn.cursor().execute(sql)
        conn.commit()
        print("result结果为:", result)
        print("sql语句:" + sql)
        conn.close()


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #访问统计
        common.tongji("exam_index")

        #代码开始
        sql="select * from exam_paper where id="+self.get_argument("id")
        exam_paper=common.find("organization",sql)
        print(exam_paper)
        self.render("organization\\templates\\Exam\\index.html",exam_paper=exam_paper)
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
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        self.write("提交完成！")

class errorRankingHandler(tornado.web.RequestHandler):
    def post(self):
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("organization/templates/Exam/error_ranking_select.html",exam_papers=exam_papers)



class singleChoiceAddHandler(tornado.web.RequestHandler):
    def post(self):
        #sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        data={}
        data["title"]=self.get_argument("title")
        data["choice1"]=self.get_argument("choice1")
        data["choice2"]=self.get_argument("choice2")
        data["choice3"]=self.get_argument("choice3")
        data["choice4"]=self.get_argument("choice4")
        data["picture"]=self.get_argument("picture","")
        data["module"]=self.get_argument("module")
        sql="insert into single_choice_question(title,choice1,choice2,choice3,choice4,picture,module) values('"+data["title"]+"','"+data["choice1"]+"','"+data["choice2"]+"','"+data["choice3"]+"','"+data["choice4"]+"','"+data["picture"]+"','"+data["module"]+"')"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("organization_admin/templates/Question/single_choice_add.html",exam_papers=exam_papers)


class selectHandler(tornado.web.RequestHandler):
    def get(self):
        # print("进入task_select_get方法了")

        impedes = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from impede where status = 'abled'")
        challenges = sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute(
            "select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        # print("challenges:",dir(challenges))

        self.render("organization/templates/Question/select.html"

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
        if self.get_argument("type")=="single_choice":
            sql="select * from single_choice_question"
            single_choice_questions=common.select("organization",sql)
        if self.get_argument("type")=="true-false":
            sql="select * from true-false_question"
            true_false_questions=common.select("organization",sql)
        if self.get_argument("type")=="operation":
            sql="select * from operation_question"
            operation_questions=common.select("organization",sql) 
               

        self.render("D:\\projects3\\organization\\templates\\Question\\result.html"
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,single_choice_questions=single_choice_questions)

        
class trueFalseAddHandler(tornado.web.RequestHandler):
    def post(self):
        #sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        data={}
        data["title"]=self.get_argument("title")
        data["answer"]=self.get_argument("answer")
        data["picture"]=self.get_argument("picture","")
        data["module"]=self.get_argument("module")
        sql="insert into tf_question(title,answer,picture,module) values('"+data["title"]+"','"+data["answer"]+"','"+data["picture"]+"','"+data["module"]+"')"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
    def get(self):
        sql="select * from exam_paper"
        print(sql)
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        exam_papers=cursor.fetchall()
        self.render("organization_admin/templates/Question/true_false_add.html",exam_papers=exam_papers)

class operationAddHandler(tornado.web.RequestHandler):
    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        print("post_data:",post_data)

        data = {}        
        # 素材文件的处理
        UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Question","material","")
        # username = self.get_argument('username', 'anonymous')
        if self.request.files.get('material', None):
            uploadFile = self.request.files['material'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["material"] =  filename
        else:
            data["material"]=""

        # 标准答案文件的处理
        UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Question","answer","")
        if self.request.files.get('correct_answer', None):
            uploadFile = self.request.files['correct_answer'][0]
            filename = uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["correct_answer"] =  filename            
        self.write("上传成功")          
        # 图片文件处理
        UPLOAD_FILE_PATH = UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Question","picture","")
        if self.request.files.get('photo1', None):
            uploadFile = self.request.files['photo1'][0]
            photo_url = uploadFile['filename']
            print(photo_url)
            fileObj = open(UPLOAD_FILE_PATH + photo_url, 'wb')
            fileObj.write(uploadFile['body'])
        else:
            photo_url=""

       
        data["title"]=self.get_argument("title")
        data["picture"]=photo_url
        data["module"]=self.get_argument("module")
        data["difficult"] = self.get_argument("difficult")


        sql="insert into operation_question(title,material,answer,picture,module,difficult_level) values('"+data["title"]+"','"+data["material"]+"','"+data["correct_answer"]+"','"+data["picture"]+"','"+data["module"]+"','"+data["difficult"]+"')"
        print(sql)
        result=common.execute("organization",sql)
        if result:
            self.write("<html><head></head><body><script>window.alert('添加成功！');window.location.href('index')</script></body></html>")
        else:
            self.write("<html><head></head><body><script>window.alert('添加失败，联系白老师！')</script></body></html>")
    def get(self):
        
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Question","operation_add.html"))        

