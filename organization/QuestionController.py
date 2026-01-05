import tornado
import sqlite3

import warnings
import os
import uuid

warnings.filterwarnings('ignore')
import time
import myportal.common as common
import json



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
        conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
        sql = "select * from single_choice_question"
        single_choice_questions=common.select("organization", sql)
        print(single_choice_questions)
        sql = "select * from tf_question"
        tf_questions=common.select("organization", sql)
        print(tf_questions)
        self.render("organization\\templates\\Question\\lists.html",single_choice_questions=single_choice_questions,tf_questions=tf_questions)



class addHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("暂无权限！请联系管理员!")

    

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
    def post(self):
        post_data = self.request.arguments
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
            #print("post_data:",post_data)
        print("post_data:",post_data)


        data = {}

        #获取uid
        if self.get_cookie("user_id",None)!=None:
            data["user_id"]=self.get_cookie("user_id")
            # 获取模块和题型
            data["question_module"] = self.get_argument("module")
            data["question_type"] = self.get_argument("type")
            print("question:",self.get_arguments("question_id"))
            print("answer:",self.get_arguments("answer"))
            print("题型：",data)
            answer={}
            #不同题型不同处理方式
            #如果是操作题
            if data["question_type"] == "operation":
                # 上传文件的处理
                UPLOAD_FILE_PATH = 'organization\\templates\\Question\\upload\\'
                # 获取所有同名文件
                files = self.request.files['file']  # 'file' 是表单中的input元素name属性值
                print("上传文件：",files)
                for i in range(len(files)):
                    # 生成新的文件名
                    filepath = str(uuid.uuid4()) + os.path.splitext(files[i]['filename'])[1]
                    # 保存文件到服务器
                    with open(os.path.join(UPLOAD_FILE_PATH, filepath), 'wb') as f:
                        f.write(files[i]['body'])
                        answer[self.get_arguments("question_id")[i]]=filepath
                        print("answer:",answer)
                self.write("上传成功")
            else:#选择或者判断
                for i in range(len(self.get_arguments("question_id"))):
                    answer[self.get_arguments("question_id")[i]]=self.get_argument("answer["+self.get_arguments("question_id")[i]+"]")
            data["question_id"]=self.get_arguments("question_id")[0]
            sql = "insert into student_answer(student_id,question_id,answer,ctime,question_type,question_module) values(" + self.get_cookie("user_id") + "," + self.get_arguments("question_id")[0] + ",'" + answer[self.get_arguments("question_id")[0]] + "','" + str(int(time.time())) + "','"+self.get_argument("type")+"','"+self.get_argument("module")+"')"
            for i in range(1,len(self.get_arguments("question_id"))):
                data["question_id"]=self.get_arguments("question_id")[i]
                data["student_id"] = self.get_cookie("user_id")
                data["ctime"] = str(int(time.time()))
                data["question_type"] = self.get_argument("type")
                data["question_module"] = self.get_argument("module")
                sql=sql+",("+data["student_id"]+","+data["question_id"]+",'"+answer[self.get_arguments("question_id")[i]]+"','"+data["ctime"]+"','"+data["question_type"]+"','"+data["question_module"]+"')"
            print(sql)
            conn = sqlite3.connect("D:\\projects3\\db\\organization.db")
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            
            if self.get_argument("type")=="single_choice":
                sql="select * from single_choice_question where module='"+data["question_module"]+"'"
                single_choice_questions=common.select("organization",sql)
            if self.get_argument("type")=="true_false":
                sql="select * from tf_question where module='"+data["question_module"]+"'"
                true_false_questions=common.select("organization",sql)
            if self.get_argument("type")=="operation":
                #取出最新的数据
                sql="select student_answer.id as id,operation_question.title as title,operation_question.module as module,operation_question.picture as picture,operation_question.material as material,student_answer.answer as student_answer,operation_question.answer as correct_answer from student_answer,operation_question where student_answer.ctime= (select MAX(student_answer.ctime) from student_answer) and student_answer.question_id=operation_question.id"
                operation_questions=common.select("organization",sql) 
                single_choice_questions = {}
                true_false_questions = {}
                #operation_questions["answer"] organization/templates/Question/upload/
                for i in range(len(operation_questions)):
                    if operation_questions[i]["module"] =="excel":
                        operation_questions[i]["difference"] = ""
                    else:
                        with open("organization/templates/Question/upload/"+operation_questions[i]["student_answer"], 'r',encoding='utf-8') as file:
                            content = file.read()
                            
                            import html
    
                            def python_to_html(code):
                                # 将文本中的回车转换为HTML的<br>标签
                                html_content = code.replace('\n', '<br>')
                                return html_content
                            html_code = python_to_html(content)
                            print(html_code)
                            operation_questions[i]["answer"] = html_code
                            import difflib
    
                            def compare_files(file1, file2):
                                with open(file1, 'r',encoding='utf-8') as f1, open(file2, 'r',encoding='utf-8') as f2:
                                    text1 = f1.readlines()
                                    text2 = f2.readlines()
                            
                                diff = difflib.unified_diff(text1, text2, fromfile=file1, tofile=file2)
                                return '\n'.join(diff)
                            
                            # 使用例子
                            file1 = "organization/templates/Question/upload/"+operation_questions[i]["student_answer"]
                            file2 = "organization/templates/Question/answer/"+operation_questions[i]["correct_answer"]
                            
                            difference = compare_files(file1, file2)
                            print("文件不同：",difference)
                            operation_questions[i]["difference"] = difference
                            import re
  
                            pattern = r'^\+'
                            matches = re.findall(pattern,difference, flags=re.MULTILINE)

                            #求出几个空：
                            with open("organization/templates/Question/upload/"+operation_questions[i]["material"],'r',encoding='utf-8') as f3:
                                text3=f3.read()
                            if text3.find("<3>")!=-1:
                                sum=3
                            elif text3.find("②")!=-1 or text3.find("<2>")!=-1:
                                sum=2
                            else:
                                sum=1


                            if len(matches)>1:
                                operation_questions[i]["score"]= 15-(len(matches)-1)*(15/sum)
                            else:
                                operation_questions[i]["score"]=15
                            if operation_questions[i]["score"]<0:
                                operation_questions[i]["score"]=0
                            print("匹配结果:",re.findall(pattern,difference, flags=re.MULTILINE))


                            def compute_similarity_score(text1, text2):
                                # 使用 difflib 生成差异
                                diff = difflib.SequenceMatcher(None, text1, text2)
                            
                                # 计算差异的分数
                                similarity = diff.ratio()
                                return similarity
                            
                            # 示例文本
                            with open(file1, 'r',encoding='utf-8') as f1, open(file2, 'r',encoding='utf-8') as f2:
                                    text1 = f1.readlines()
                                    text2 = f2.readlines()
                            
                            # 计算相似度分数
                            score = compute_similarity_score(text1, text2)
                            print("score:",score)
                            print(f"Similarity score: {score*100:.2f}%")
                        
            print("结果集single_choice_questions",single_choice_questions)       
            print("结果集true_false_questions",true_false_questions)
            print("结果集operation_questions",operation_questions)

            self.render("D:\\projects3\\organization\\templates\\Question\\answer_lists.html"
            ,module=data["question_module"]
            ,question_type=self.get_argument("type")
            ,operation_questions=operation_questions
            ,true_false_questions=true_false_questions
            ,single_choice_questions=single_choice_questions)                                  
        else:
            self.write("登录已经过期，请重新<a href='/organization/Index/login'>登录</a>！")



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
        sql="insert into examinee_answer(ctime,student_name,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve,thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen,twenty,twentyone,twentytwo,exam_paper_id,grade,class) values("+data["ctime"]+",'"+data["student_name"]+"','"+data["one"]+"','"+data["two"]+"','"+data["three"]+"','"+data["four"]+"','"+data["five"]+"','"+data["six"]+"','"+data["seven"]+"','"+data["eight"]+"','"+data["nine"]+"','"+data["ten"]+"','"+data["eleven"]+"','"+data["twelve"]+"','"+data["thirteen"]+"','"+data["fourteen"]+"','"+data["fifteen"]+"','"+data["sixteen"]+"','"+data["seventeen"]+"','"+data["eighteen"]+"','"+data["nineteen"]+"','"+data["twenty"]+"','"+data["twentyone"]+"','"+data["twentytwo"]+"',"+self.get_argument("exam_paper_id")+",'"+self.get_argument("grade")+"','"+self.get_argument("class")+"')";
        sql="insert into single_choice_question()"
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
        self.render("organization/templates/Question/single_choice_add.html",exam_papers=exam_papers)

class selectModuleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization","templates","Question","select_module.html"))

class selectDifficultHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization","templates","Question","select_difficult.html"),module=self.get_argument("module"))
        
    def post(post):
        pass


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

