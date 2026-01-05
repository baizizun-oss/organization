import tornado
import sqlite3
import os
import warnings

warnings.filterwarnings('ignore')
import time
import myportal.common as common

class commonHandler():
    def tongji(modulename):
        # 统计模块开始
        conn = sqlite3.connect(
            "D:\\projects3\\db\\baigaopeng_myportal.db")
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'"+modulename+"')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from operation_question"
        questions=common.select("organization",sql)
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Exam","lists.html"),
                    questions=questions
                    )


class addQuestionHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from operation_question"
        questions=common.select("organization",sql)
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","Exam","operation_add.html"),
                    questions=questions
                    )


class examPaperAddHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入task_index_add_get")
        commonHandler.tongji("exam_paper_add")
        self.render("sangao_admin/templates/Exam/exam_paper_add.html")
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
        data["twentyone_sucai"]=""
        data["twentytwo_sucai"]=""
        data["true-false1"]=""
        data["true-false2"]=""
        data["true-false3"]=""
        data["true-false4"]=""
        data["true-false5"]=""
        data["zonghe1-1"]=""
        data["zonghe1-2"]=""
        data["zonghe1-3"]=""
        data["zonghe1-4"]=""
        data["zonghe1-5"]=""
        data["zonghe1-6"]=""
        data["zonghe2-1"]=""
        data["zonghe2-2"]=""
        data["zonghe2-3"]=""
        data["zonghe2-4"]=""
        data["zonghe2-5"]=""
        data["zonghe2-6"]=""

        UPLOAD_FILE_PATH = 'sangao\\templates\\Exam\\upload\\'
        if self.request.files.get('one', None):
            uploadFile = self.request.files['one'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["one"]=filename
        if self.request.files.get('two', None):
            uploadFile = self.request.files['two'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["two"]=filename
        if self.request.files.get('three', None):
            uploadFile = self.request.files['three'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["three"]=filename
        if self.request.files.get('four', None):
            uploadFile = self.request.files['four'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["four"]=filename
        if self.request.files.get('five', None):
            uploadFile = self.request.files['five'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["five"]=filename
        if self.request.files.get('six', None):
            uploadFile = self.request.files['six'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["six"]=filename
        if self.request.files.get('seven', None):
            uploadFile = self.request.files['seven'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["seven"]=filename
        if self.request.files.get('eight', None):
            uploadFile = self.request.files['eight'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["eight"]=filename
        if self.request.files.get('nine', None):
            uploadFile = self.request.files['nine'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["nine"]=filename
        if self.request.files.get('ten', None):
            uploadFile = self.request.files['ten'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["ten"] = filename
        if self.request.files.get('eleven', None):
            uploadFile = self.request.files['eleven'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["eleven"] = filename
        if self.request.files.get('twelve', None):
            uploadFile = self.request.files['twelve'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twelve"] = filename
        if self.request.files.get('thirteen', None):
            uploadFile = self.request.files['thirteen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["thirteen"] = filename
        if self.request.files.get('fourteen', None):
            uploadFile = self.request.files['fourteen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["fourteen"] = filename
        if self.request.files.get('fifteen', None):
            uploadFile = self.request.files['fifteen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["fifteen"] = filename
        if self.request.files.get('sixteen', None):
            uploadFile = self.request.files['sixteen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["sixteen"] = filename
        if self.request.files.get('seventeen', None):
            uploadFile = self.request.files['seventeen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["seventeen"] = filename
        if self.request.files.get('eighteen', None):
            uploadFile = self.request.files['eighteen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["eighteen"] = filename
        if self.request.files.get('nineteen', None):
            uploadFile = self.request.files['nineteen'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["nineteen"] = filename
        if self.request.files.get('twenty', None):
            uploadFile = self.request.files['twenty'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twenty"] = filename
        if self.request.files.get('twentyone', None):
            uploadFile = self.request.files['twentyone'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twentyone"] = filename
        if self.request.files.get('twentytwo', None):
            uploadFile = self.request.files['twentytwo'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twentytwo"] = filename
        if self.request.files.get('twentyone_sucai', None):
            uploadFile = self.request.files['twentyone_sucai'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twentyone_sucai"] = filename
        if self.request.files.get('twentytwo_sucai', None):
            uploadFile = self.request.files['twentytwo_sucai'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["twentytwo_sucai"] = filename
        if self.request.files.get('true-false1', None):
            uploadFile = self.request.files['true-false1'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["true-false1"] = filename
        if self.request.files.get('true-false2', None):
            uploadFile = self.request.files['true-false2'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["true-false2"] = filename
        if self.request.files.get('true-false3', None):
            uploadFile = self.request.files['true-false3'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["true-false3"] = filename
        if self.request.files.get('true-false4', None):
            uploadFile = self.request.files['true-false4'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["true-false4"] = filename
        if self.request.files.get('true-false5', None):
            uploadFile = self.request.files['true-false5'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["true-false5"] = filename        
        if self.request.files.get('zonghe1-1', None):
            uploadFile = self.request.files['zonghe1-1'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe1-1"] = filename        
        if self.request.files.get('zonghe1-2', None):
            uploadFile = self.request.files['zonghe1-2'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe1-2"] = filename 
        if self.request.files.get('zonghe1-3', None):
            uploadFile = self.request.files['zonghe1-3'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe1-3"] = filename 
        if self.request.files.get('zonghe1-4', None):
            uploadFile = self.request.files['zonghe1-4'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe1-4"] = filename                
        if self.request.files.get('zonghe1-5', None):
            uploadFile = self.request.files['zonghe1-5'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe1-5"] = filename 
        if self.request.files.get('zonghe1-6', None):
            uploadFile = self.request.files['zonghe1-6'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe1-6"] = filename 
        if self.request.files.get('zonghe2-1', None):
            uploadFile = self.request.files['zonghe2-1'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe2-1"] = filename       
        if self.request.files.get('zonghe2-2', None):
            uploadFile = self.request.files['zonghe2-2'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe2-2"] = filename 
        if self.request.files.get('zonghe2-3', None):
            uploadFile = self.request.files['zonghe2-3'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe2-3"] = filename 
        if self.request.files.get('zonghe2-4', None):
            uploadFile = self.request.files['zonghe2-4'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe2-4"] = filename        
        if self.request.files.get('zonghe2-5', None):
            uploadFile = self.request.files['zonghe2-5'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe2-5"] = filename  
        if self.request.files.get('zonghe2-6', None):
            uploadFile = self.request.files['zonghe2-6'][0]
            filename = data["title"]+"_"+uploadFile['filename']
            fileObj = open(UPLOAD_FILE_PATH + filename, 'wb')
            fileObj.write(uploadFile['body'])
            data["zonghe2-6"] = filename            
                                                                                                                                   
        print(data)
        sql = "insert into exam_paper(title,ctime,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,twentyone_sucai,twentytwo_sucai,'true-false1','true-false2','true-false3','true-false4','true-false5','zonghe1-1','zonghe1-2','zonghe1-3','zonghe1-4','zonghe1-5','zonghe1-6','zonghe2-1','zonghe2-2','zonghe2-3','zonghe2-4','zonghe2-5','zonghe2-6') values('"+data["title"] +"',"+data["ctime"]+\
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
        "','"+data["twentyone_sucai"]+\
        "','"+data["twentytwo_sucai"]+\
        "','"+data["true-false1"]+\
        "','"+data["true-false2"]+\
        "','"+data["true-false3"]+\
        "','"+data["true-false4"]+\
        "','"+data["true-false5"]+\
        "','"+data["zonghe1-1"]+\
        "','"+data["zonghe1-2"]+\
        "','"+data["zonghe1-3"]+\
        "','"+data["zonghe1-4"]+\
        "','"+data["zonghe1-5"]+\
        "','"+data["zonghe1-6"]+\
        "','"+data["zonghe2-1"]+\
        "','"+data["zonghe2-2"]+\
        "','"+data["zonghe2-3"]+\
        "','"+data["zonghe2-4"]+\
        "','"+data["zonghe2-5"]+\
        "','"+data["zonghe2-6"]+\
        "')"
        print("sql语句:" + sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        result = conn.cursor().execute(sql)
        print("result:", result)

        conn.commit()
        conn.close()
        self.write("添加成功")


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
        commonHandler.tongji("exam_paper_del")
        sql = "delete from exam_paper where id=" + self.get_argument("id")
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
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
        sql="select * from exam_paper"
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
'''
	public function error_ranking_list(){
		if ($_POST){
			//从数据库中获取学生考试数据
			$student_answer=M("ExamineeAnswer")->where("grade='".$_POST["grade"]."' and exam_paper_id=".$_POST["exam_paper_id"])->select();
			/*统计出各道题的错误数量并记入向前端传输的数组中*/
			//先找出标准答案
			$system_answer=M("ExamPaper")->where("id=".$_POST["exam_paper_id"])->find();
			//初始个数都为0，每有一人错误就增加一次
			$error_number["one"]=0;//第一题的错误数量
			$error_number["two"]=0;//第二题的错误数量
			$error_number["three"]=0;
			$error_number["four"]=0;
			$error_number["five"]=0;
			$error_number["six"]=0;
			$error_number["seven"]=0;
			$error_number["eight"]=0;
			$error_number["nine"]=0;
			$error_number["ten"]=0;
			$error_number["eleven"]=0;
			$error_number["twelve"]=0;
			$error_number["thirteen"]=0;
			$error_number["fourteen"]=0;
			$error_number["fifteen"]=0;
			$error_number["sixteen"]=0;
			$error_number["seventeen"]=0;
			$error_number["eighteen"]=0;
			$error_number["nineteen"]=0;
			$error_number["twenty"]=0;
			//循环处理每份学生答案
			foreach ($student_answer as $key=>$value){
				if ($value["one"]!==$system_answer["one_answer"]) $error_number["one"]=$error_number["one"]+1;
				if ($value["two"]!==$system_answer["two_answer"]) $error_number["two"]=$error_number["two"]+1;
				if ($value["three"]!==$system_answer["three_answer"]) $error_number["three"]=$error_number["three"]+1;
				if ($value["four"]!==$system_answer["four_answer"]) $error_number["four"]=$error_number["four"]+1;
				if ($value["five"]!==$system_answer["five_answer"]) $error_number["five"]=$error_number["five"]+1;
				if ($value["six"]!==$system_answer["six_answer"]) $error_number["six"]=$error_number["six"]+1;
				if ($value["seven"]!==$system_answer["seven_answer"]) $error_number["seven"]=$error_number["seven"]+1;
				if ($value["eight"]!==$system_answer["eight_answer"]) $error_number["eight"]=$error_number["eight"]+1;
				if ($value["nine"]!==$system_answer["nine_answer"]) $error_number["nine"]=$error_number["nine"]+1;
				if ($value["ten"]!==$system_answer["ten_answer"]) $error_number["ten"]=$error_number["ten"]+1;
				if ($value["eleven"]!==$system_answer["eleven_answer"]) $error_number["eleven"]=$error_number["eleven"]+1;
				if ($value["twelve"]!==$system_answer["twelve_answer"]) $error_number["twelve"]=$error_number["twelve"]+1;
				if ($value["thirteen"]!==$system_answer["thirteen_answer"]) $error_number["thirteen"]=$error_number["thirteen"]+1;
				if ($value["fourteen"]!==$system_answer["fourteen_answer"]) $error_number["fourteen"]=$error_number["fourteen"]+1;
				if ($value["fifteen"]!==$system_answer["fifteen_answer"]) $error_number["fifteen"]=$error_number["fifteen"]+1;
				if ($value["sixteen"]!==$system_answer["sixteen_answer"]) $error_number["sixteen"]=$error_number["sixteen"]+1;
				if ($value["seventeen"]!==$system_answer["seventeen_answer"]) $error_number["seventeen"]=$error_number["seventeen"]+1;
				if ($value["eighteen"]!==$system_answer["eighteen_answer"]) $error_number["eighteen"]=$error_number["eighteen"]+1;
				if ($value["nineteen"]!==$system_answer["nineteen_answer"]) $error_number["nineteen"]=$error_number["nineteen"]+1;
				if ($value["twenty"]!==$system_answer["twenty_answer"]) $error_number["twenty"]=$error_number["twenty"]+1;
			}
			//所有考卷处理完得出错误总数排序后送到前端
			arsort($error_number);//根据值对此数组进行关联降序
			$this->assign("error_number",$error_number);
			$this->mydisplay();
		}
	else {
		$exam_paper=M("ExamPaper")->select();
		$this->assign("exam_paper",$exam_paper);
		$this->mydisplay("error_ranking_select");
		}
		
		
	}

'''
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
