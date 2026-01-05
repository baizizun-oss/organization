import tornado
import sqlite3
import requests
import warnings
import os
import random
import json
import uuid
import logging
import asyncio
import myportal.common as common
warnings.filterwarnings('ignore')
import time



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

class questionListsHandler(tornado.web.RequestHandler):
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



class selectModuleHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization","templates","Exam","select_module.html"))

class selectDifficultHandler(tornado.web.RequestHandler):
    def get(self):

        self.render(os.path.join(common.BASE_DIR,"organization","templates","Exam","select_difficult.html"),module=self.get_argument("module"))
        
    def post(post):
        pass



class examPaperListsHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/sangao/Index/login'>登录</a>")
            #self.render("sangao/templates/Index/login.html")
        else:

            # 统计模块开始
            conn = sqlite3.connect(
                "D:\\projects3\\db\\baigaopeng_myportal.db")
            sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'exam_paper_lists')"
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
        commonHandler.tongji("exam_paper_add")
        self.render("sangao/templates/Exam/exam_paper_add.html")
    def post(self):
        data={}
        data["title"]=self.get_argument("title")
        data["ctime"]=int(time.time())
        data["author"]=self.get_argument("author")
        sql="insert into exam_paper(title,author,ctime) values('"+data["title"]+"','"+data["author"]+"',"+data["ctime"]+")"
        print("sql语句:" + sql)
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        result = conn.cursor().execute(sql)
        print("result:", result)

        conn.commit()
        conn.close()
        self.write("添加成功")

class examPaperEditHandler(tornado.web.RequestHandler):
    def get(self):
        conn = sqlite3.connect("D:\\projects3\\db\\sangao.db")
        cursor=conn.cursor()
        sql="select * from exam_plan where exam_paper_id="+self.get_argument("exam_paper_id")
        result=cursor.execute(sql)
        design=cursor.fetchall()
        print(design)
        self.render("sangao/templates/Exam/exam_paper_edit.html"
                    , questions=design
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
        print("cookie:",self.get_cookie("user_id"))
        if not self.get_cookie("user_id",None):
            self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('没有登陆或者已经过期，请登陆！');window.location.href = '/organization/Index/login';</script></body></html>") 
        else:
            module=self.get_argument("module")
            if module=="python":
                #考试开始前先将session过期的时间修改为一小时，以免写完提交时已经失去用户信息而提交失败
                #self.set_cookie(expires=3600000,name="user_id",value=self.get_cookie("user_id"))
                sql="select * from question where difficult="+self.get_argument("difficult")+" and type='"+self.get_argument("module")+"'"
                #print("sql:",sql)
                questions = common.select("organization",sql)
                #print("结果集：",operation_questions)
                question = questions[random.randint(0,len(questions)-1)]
                self.render(os.path.join(common.BASE_DIR,"organization","templates","Exam","index.html"),question=question,module=self.get_argument("module"),question_type="operation")
            if module=="scratch":
                #考试开始前先将session过期的时间修改为一小时，以免写完提交时已经失去用户信息而提交失败
                #self.set_cookie(expires=3600000,name="user_id",value=self.get_cookie("user_id"))
                sql="select * from operation_question where difficult_level="+self.get_argument("difficult")+" and module='"+self.get_argument("module")+"'"
                #print("sql:",sql)
                questions = common.select("organization",sql)
                #print("结果集：",operation_questions)
                question = questions[random.randint(0,len(questions)-1)]
                self.render(os.path.join(common.BASE_DIR,"organization","templates","Exam","scratch_operation.html"),question=question,module=self.get_argument("module"),question_type="operation")
                 

    async def post(self):
        module=self.get_argument('module')
        if module=="python":
            sql="select * from question where id="+self.get_argument("question_id")
            question = common.find("organization",sql)    
            # 1. 接收上传文件
            upload = self.request.files['user_code'][0]
            code = upload['body'].decode('utf-8')
            


            # 2. 生成随机文件名（避免冲突）（一个随机目录+固定文件名）
            file_id = str(int(time.time()))
            os.makedirs(f"/tmp/{file_id}", exist_ok=True)
            code_path = f"/tmp/{file_id}/oj_{file_id}.{self.get_argument('module')}"
            
            with open(code_path, 'w') as f:
                f.write(code)
            # 如1果此题有输入则需要将输入文件复制到临时文件夹（用户程序所在的目录），以便用户程序可以方便的打开输入文件（用open("data.in")不用加任何路径）此环节必须在开始容器前进行
            if question["test_data_input"]:
                with open(question["test_data_input"],"r") as in_file:
                    with open(f"/tmp/{file_id}/data.in","w") as tmp_in_file:
                        tmp_in_file.write(in_file.read())        

            # 3. 执行判题
            result = await self._run_in_container(
                code_path=code_path,
                language=self.get_argument('module')
            )

        

        
            score=0
            # 将用户程序的输出结果和预设output进行对比
            with open(question["test_data_output"],"r") as out_file:
                lines=out_file.readlines()
                for i in range(len(lines)):
                    print("lines[i]:",lines[i])
                    print("output:",result["output"].split()[i])
                    if lines[i].split()[0]==result["output"].split()[i]:
                        score=score+100/len(lines)

            if score>90:
                sql="update user set current_level='"+question["difficult"]+"'"
                result=common.execute("organization",sql)
                if result:
                    self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('恭喜晋级为"+str(question["difficult"])+"！');window.location.href = '/organization/Index/login';</script></body></html>") 
            else:
                print("result:",result)
                # 4. 返回结果
                self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('得分"+str(score)+"！');window.location.href = '/organization/Index/login';</script></body></html>") 
        if module=="scratch":
            pass
        if module=="ev3":
            pass


    async def _run_in_container(self, code_path, language):
        # 修正命令构建方式
        filename = os.path.basename(code_path)
        dir_path = os.path.dirname(code_path)
        #dir_path = os.path.join(os.path.dirname(code_path),file_id)
        
        if language == "python":
            cmd = f"python3 {filename}"
            #cmd = f"tail -f /dev/null"
            image = "oj_python:1.0"
        elif language == "cpp":
            cmd = "g++ /code/main.cpp -o /code/a.out && /code/a.out"
            image = "gcc:latest"
        else:
            return {"error": "unsupported language"}
        
        docker_cmd = f"""
        docker run --rm \
            -v {dir_path}/:/code/ \
            -w /code \
            {image} \
            sh -c "{cmd}"
        """
        
        proc = await asyncio.create_subprocess_shell(
            docker_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await proc.communicate()
        
        return {
            "output": stdout.decode(),
            "error": stderr.decode(),
            "exit_code": proc.returncode
        }



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


        # print("tasks is:",tasks)
        ##print#print("data is:",data)
        self.render("sangao/Learn/templates/result.html"
                    , tasks=tasks)
        #	       #conn.


