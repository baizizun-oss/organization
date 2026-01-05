# -*-coding:utf8;-*-
# qpy:console


import os.path
import logging
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
import traceback
import time
import json
import sqlite3
import myportal.common as common

logger = logging.getLogger(__name__)
class listsHandler(tornado.web.RequestHandler):
    def get(self):
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
        else:
            users = common.select("organization","select * from user order by status desc,campus desc,points desc")

            self.render(os.path.join("organization_admin","templates","User","lists.html"),users=users)


class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'myportal_Index_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","index.html"))
    def on_response(self,response):
        body= json.loads(response.body)
        print("response内容为:",body)
        self.finish


class clickSelectHandler(tornado.web.RequestHandler):
    def get(self):
        # 统计模块开始
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        sql = "insert into click(click_time,click_action) values(" + str(int(time.time())) + ",'click_select')"
        result = conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        # 统计模块结束
        print("now is accessing myportal_index_click_select_get")
        self.render("myportal/templates/Index/click_select.html")

    def post(self):
        print("now is accessing myporta_index_click_select_post")
        data = {}
        # start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        # data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        # end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        # data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        # data["start_time"]=self.get_argument("start_time")
        # data["end_time"]=self.get_argument("end_time")

        # sql="insert into holiday(start_time,end_time) values("+data["start_time"]+","+data["end_time"]+")"
        sql = "select count(*) as fangwen_num,click_action from click group by click_action"
        print("sql sentence:", sql)
        conn = sqlite3.connect(os.path.join(common.BASE_DIR,"organization","db","organization.db"))
        cursor = conn.cursor()
        cursor.execute(sql)
        for row in cursor.fetchall():  # 从fetchall中读取操作 print(row)
            print("result:", row)
            # self.write(row)
        conn.commit()
        conn.close()
        # self.write("添加成功！")
        # self.write(result)



class checkPassHandler(tornado.web.RequestHandler):
    def get(self):
        sql="update user set status='checked' where id="+self.get_argument("id")
        common.execute("organization",sql)
        self.write("修改成功！")



class editHandler(tornado.web.RequestHandler):
    def get(self):
        sql = "select * from user where id="+self.get_argument("id")
        user = common.find("organization",sql)
        self.render("organization_admin/templates/User/edit.html",user=user)

    # def post(self):
    #     sql="update user set status = '"+ self.get_argument("status") + "' where id="+self.get_argument("id")+";"
    #     #在用户状态变化中作记录
    #     sql+="insert into user_status_history(user_id,ctime,status,reason) values("+str(self.get_argument("id"))+","+str(int(time.time()))+",'"+self.get_argument("status")+"','"+self.get_argument("reason")+"');"
    #     print("sql:",sql)
    #     result = common.execute("organization",sql)
    #     if result:
    #         self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");</script></body></html>')


    def post(self):
        user_id = self.get_argument("id")
        status = self.get_argument("status")
        reason = self.get_argument("reason", default="")

        # 构造安全的参数化语句列表
        statements = [
            ("UPDATE user SET status = ? WHERE id = ?", (status, user_id)),
            (
                "INSERT INTO user_status_history (user_id, ctime, status, reason) VALUES (?, ?, ?, ?)",
                (user_id, int(time.time()), status, reason)
            )
        ]
        logger.info(f"sql:{statements}")
        try:
            common.executes("organization", statements)
            self.write('<html><head><title>提醒</title></head><body><script>alert("修改成功！");</script></body></html>')
        except Exception as e:
            print("数据库错误:", e)
            print("[ERROR] 修改用户状态失败:")
            traceback.print_exc()  # 👈 这会输出详细错误位置和原因            
            self.set_status(500)
            self.write('<html><body><script>alert("修改失败！");</script></body></html>')            