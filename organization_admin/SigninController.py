import tornado
import sqlite3
import os
from datetime import datetime
import myportal.common as common
import time
from organization_admin.RemoveMemberService import RemoveMemberService


#包含所有人的
class listsHandler(tornado.web.RequestHandler):
    def get(self):
        sql='''SELECT strftime('%Y-%m-%d', sp.expected_signin_time, 'unixepoch') AS expected_signin_time,
       u.id AS user_id,
       u.status as user_status,
       u.name AS user_name,
       CASE
           WHEN c.user_id IS NOT NULL THEN '已签到'
           ELSE '未签到'
           END AS sign_status
FROM "user" u
         CROSS JOIN signin_plan sp
         LEFT JOIN click c ON u.id = c.user_id AND strftime('%Y-%m-%d', c.click_time, 'unixepoch') = strftime('%Y-%m-%d', sp.expected_signin_time, 'unixepoch')
GROUP BY strftime('%Y-%m-%d', sp.expected_signin_time, 'unixepoch'), u.id, u.name, sign_status order by sp.expected_signin_time asc;'''
        users=common.select("organization",sql)
        print("users:",users)
        self.render("organization_admin/templates/signin_lists.html",users=users)    

#只是单人
class listHandler(tornado.web.RequestHandler):
    def get(self):
        sql = "SELECT strftime('%Y-%m-%d', click_time, 'unixepoch') AS date,COUNT(*) AS click_count, id FROM click where user_id = "+self.get_argument("id") + " group by date"
        clicks=common.select("organization",sql)
        print("clicks:",clicks)
        self.render("organization_admin/templates/signin_history.html",clicks=clicks)        


class expectedSigninlistsHandler(tornado.web.RequestHandler):
    def get(self):
      
        sql="select strftime('%Y-%m-%d', expected_signin_time, 'unixepoch') AS date,id from signin_plan order by expected_signin_time"
        expected_signin_times=common.select("organization",sql)
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","expected_signin_time_lists.html"),
                    excepted_signin_times=expected_signin_times
                    )


class addExpectedSigninHandler(tornado.web.RequestHandler):
    def get(self):
        sql = "select click.id as id,click.click_time,click.click_action,user.name as name from click,user where click.user_id=user.id"
        clicks=common.select("organization",sql)
        self.render("organization_admin/templates/add_expected_signin.html",clicks=clicks)
    def post(self):
        print("进入myportal_holiday_doubleadd_post方法了")
        
        #print("now is accessing myportal_holiday_doubleadd_post")
        data={}
        start_time = self.get_argument("start_time_year")+","+self.get_argument("start_time_month")+","+self.get_argument("start_time_day")+","+self.get_argument("start_time_hour")+","+self.get_argument("start_time_minute")
        data["start_time"] = str(int(time.mktime(time.strptime(start_time,"%Y,%m,%d,%H,%M"))))
        #end_time = self.get_argument("end_time_year")+","+self.get_argument("end_time_month")+","+self.get_argument("end_time_day")+","+self.get_argument("end_time_hour")+","+self.get_argument("end_time_minute")
        #data["end_time"] = str(int(time.mktime(time.strptime(end_time,"%Y,%m,%d,%H,%M"))))
        

        
        
        sql="insert into signin_plan(expected_signin_time) values("+data["start_time"]+");"

        print("sql sentence:",sql)
        try:
            result=common.execute("organization",sql)
            if result:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("添加成功！");</script></body></html>')  
        except:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("数据库执行出错！");</script></body></html>')  
        
        # 3. 添加成功后，检查并处理连续未签到的成员
        try:
            members_to_remove = RemoveMemberService.get_should_remove_members()
            print("要除名的成员：",members_to_remove)
            removed_count = 0
            for user_id, user_name in members_to_remove:
                remove_success = RemoveMemberService.remove_member(user_id)
                if remove_success:
                    removed_count += 1
                    print(f"在添加新签到计划后，用户 {user_name}(ID:{user_id}) 因连续三次未签到已被自动除名。")
            print("除名数量：",removed_count)
            if removed_count > 0:
                # 可以选择在页面上提示除名信息，或者仅记录日志
                self.write(f'<script>alert("添加成功！系统已自动处理 {removed_count} 名连续缺勤成员。"); window.location.href="/organization_admin/Index/signin_manager";</script>')
            else:
                self.write('<script>alert("添加成功！"); window.location.href="/organization_admin/Index/signin_manager";</script>')

        except Exception as e:
            # 即使除名检查出错，也不影响主流程，但应记录日志并提示用户
            print(f"添加签到计划后检查除名时出错: {e}")
            self.write('<script>alert("添加成功，但后续除名检查遇到问题，请查看日志。"); window.location.href="/organization_admin/Index/signin_manager";</script>')



