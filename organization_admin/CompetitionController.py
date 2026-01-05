import tornado
import sqlite3
import urllib
import requests
import warnings
import os
import uuid

warnings.filterwarnings('ignore')
import time
import myportal.common as common
import json



class listsHandler(tornado.web.RequestHandler):
    def get(self):
        #统计
        common.tongji("competition_lists")

        sql = "select * from competition"
        competitions = common.select("organization",sql)

        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Competition","lists.html"),competitions=competitions)




class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Competition","add.html"))

    def post(self):
        data={}
        data["name"]=self.get_argument("name")
        start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")
        data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d"))))
        end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")
        data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d"))))
        data["require"] = self.get_argument("require").replace("'","''")
        data["suggest"] = self.get_argument("suggest")
        data["host"]=self.get_argument("host")
        sql="insert into competition(name,start_time,end_time,require,suggest,host,cost) values('"+data["name"]+"',"+data["start_time"]+","+data["end_time"]+",'"+data["require"]+"','"+data["suggest"]+"','"+data["host"]+"',100)"
        result = common.execute("organization",sql)
        if result:
            self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('添加成功！');window.location.href = 'lists';</script></body></html>") 
        else:
            self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('添加失败，联系白老师！');window.location.href = 'lists';</script></body></html>") 

class editHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from competition where id="+self.get_argument("id")
        competition = common.find("organization",sql)
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Competition","edit.html"),competition=competition)
    def post(self):
        data={}
        data["name"]=self.get_argument("name")
        start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")
        data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d"))))
        end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")
        data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d"))))
        # data["require"] = self.get_argument("require")
        data["suggest"] = self.get_argument("suggest")
        data["introduct"] = ""
        #规则文件的处理
        UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Competition","upload","")        
        if self.request.files.get('require', None):
            uploadFile = self.request.files['require'][0]
            filename = uploadFile['filename']
            timestamp = int(time.time())
            write_path = UPLOAD_FILE_PATH  + str(timestamp)+filename
            save_path = str(timestamp)+filename
            fileObj = open(write_path, 'wb')
            fileObj.write(uploadFile['body'])
            self.write("上传成功")
            data["require"] = save_path
        else:
            self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('请上传规则文件');window.location.href = 'lists';</script></body></html>")        
        # #介绍视频的处理
        # UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization_admin","templates","Competition","upload","")        
        # if self.request.files.get('file', None):
        #     uploadFile = self.request.files['file'][0]
        #     filename = uploadFile['filename']
        #     timestamp = int(time.time())
        #     write_path = UPLOAD_FILE_PATH  + str(timestamp)+filename
        #     save_path = str(timestamp)+filename
        #     fileObj = open(write_path, 'wb')
        #     fileObj.write(uploadFile['body'])
        #     self.write("上传成功")
        #     data["introduct"] = save_path
        # else:
        #     data["introduct"] = ""
    
        sql="update competition set name='"+data["name"]+"',start_time="+data["start_time"]+",end_time="+data["end_time"]+",require='"+data["require"]+"',suggest='"+data["suggest"]+",introduct='"+data["introduct"]+"'' where id="+self.get_argument("id")
        print("sql:",sql)
        resutl=common.execute("organization",sql)
        if resutl:
            self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('修改成功！');window.location.href = 'lists';</script></body></html>") 
        else:
            self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('修改失败，请联系白老师！');window.location.href = 'lists';</script></body></html>") 

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





class selectHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            # print("进入task_select_get方法了")
            #modules=common.select("organization","select module from operation")
            
            self.render("organization/templates/Question/select.html"

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
            single_choice_questions=common.select("organization",sql)
        if self.get_argument("type")=="true_false":
            sql="select * from tf_question where module='"+data["module"]+"'"
            true_false_questions=common.select("organization",sql)
        if self.get_argument("type")=="operation":
            sql="select * from operation_question where module='"+data["module"]+"'"
            operation_questions=common.select("organization",sql) 
        print("结果集single_choice_questions",single_choice_questions)       
        print("结果集true_false_questions",true_false_questions)
        print("结果集operation_questions",operation_questions)

        self.render(os.path.join(common.BASE_DIR,"organization","templates","Question","result.html")
        ,module=data["module"]
        ,question_type=self.get_argument("type")
        ,operation_questions=operation_questions
        ,true_false_questions=true_false_questions
        ,single_choice_questions=single_choice_questions)

