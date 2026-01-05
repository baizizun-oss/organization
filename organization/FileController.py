import tornado
import sqlite3
import urllib
import requests
import warnings
warnings.filterwarnings('ignore')
import time
import myportal.common as common
import os
import logging
import subprocess
from organization.FileSyncService import FileSyncService

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'fileserver_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        # if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
        #     print("没有cookie")
        #     self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
        #     #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        # else:
        #     self.render("fileserver/templates/index.html")
        self.render("fileserver/templates/index.html")

class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        self.render(os.path.join(common.BASE_DIR,"organization","templates","File","add.html"),uid=self.get_argument("uid"))
    def post(self):

        print("进入fileserver_index_doubleadd_post 方法了")
        #上传文件的处理
        UPLOAD_FILE_PATH = os.path.join(common.BASE_DIR,"organization","templates","File","upload","")
        
        #username = self.get_argument('username', 'anonymous')
        if self.request.files.get('file', None):
            uploadFile = self.request.files['file'][0]
            filename = uploadFile['filename']
            timestamp = int(time.time())
            write_path = UPLOAD_FILE_PATH  + str(timestamp)+filename
            save_path = str(timestamp)+filename
            fileObj = open(write_path, 'wb')
            fileObj.write(uploadFile['body'])

        self.write("上传成功")
        data={}

        data["filepath"] = save_path
        data["ctime"] = str(int(time.time()))
        if self.get_argument("easy_memorize_name")=="":
            data["easy_memorize_name"] = "无名"
        else:
            data["easy_memorize_name"]=self.get_argument("easy_memorize_name")

        sql="insert into file(filepath,easy_memorize_name,uid,ctime,download_number,confirmed,access_level) values('"+data["filepath"]+"' \
        	,'"+data["easy_memorize_name"]+"',"+self.get_argument("uid")+" \
        	,"+data["ctime"]+",1 \
        	,'uncomfirmed','private')"
        print("sql语句:"+sql)
        conn=sqlite3.connect(os.path.join("db","organization.db"))
        result=conn.cursor().execute(sql)
        print("result:",result)
        
        conn.commit()
        conn.close()
        # 新增：调用同步脚本（非阻塞）
        print("文件：",write_path)
        # 在文件保存后，获取文件ID
        file_id = None
        try:
            # 连接数据库获取最后插入的文件ID
            conn = sqlite3.connect(os.path.join("db", "organization.db"))
            cursor = conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            file_id = cursor.fetchone()[0]
        except Exception as e:
            # 记录获取文件ID失败错误
            logging.error(f"获取文件ID失败: {str(e)}")
        finally:
            # 确保关闭数据库连接
            if conn:
                conn.close()
        
        # 调用同步服务
        if file_id:
            # 异步调用文件同步
            tornado.ioloop.IOLoop.current().spawn_callback(
                self._async_sync_file, write_path, file_id
            )
        
        # 返回上传成功消息
        self.write("上传成功，同步任务已启动")
    
    async def _async_sync_file(self, file_path, file_id):
        """
        异步执行文件同步
        避免阻塞主线程
        """
        # 在后台线程中执行同步操作
        await tornado.ioloop.IOLoop.current().run_in_executor(
            None,  # 使用默认线程池
            #FileSyncService.FileSyncService.sync_service.sync_file,  # 调用同步服务
            FileSyncService.FileSyncService.sync_file,
            file_path,
            file_id
        )

        
class delHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入warehouse_index_add_get")
        sql="delete from file where id="+self.get_argument("id")
        result=common.execute("organization",sql)
        if result:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("删除成功！");</script></body></html>')
        else:
            self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("系统出错，请联系老师！");</script></body></html>')

                        

        
class editHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_edit_get方法了")
        
    def post(self):
        print("进入fileserver_edit_post方法了")

        data={}
        data["start_display_time"] = self.get_argument("start_display_time")
        #data["start_display_time"] = str(int(time.mktime(time.strptime(self.get_argument("start_display_time"),"%Y,%m,%d,%H"))))
        data["title"] = self.get_argument("title")
        data["content"] = self.get_argument("content")
        data["id"] = self.get_argument('id')
        data["challenge"]=self.get_argument("challenge")
        data["impede"]=self.get_argument("impede")
        data["address"]=",".join(self.get_arguments("address[]"))
        data["status"]=self.get_argument("status")

        sql = "update task set title='"+data["title"]+"'"
        sql=sql+",content='"+data["content"].replace(" ","&nbsp").replace("\n","<br>").replace("'","&apos")+"'"
        sql=sql+",start_display_time=" + data["start_display_time"] 
        sql=sql+",status = '"+self.get_argument("status")+ "'"
        sql=sql+",impede='"+self.get_argument("impede")+"' "
        sql=sql+",address='"+",".join(self.get_arguments("address"))+"'"
        print("地点post数据",self.get_arguments("address"))
        sql=sql+",challenge='"+self.get_argument("challenge")+"'"
        sql=sql+" where id="+str(data["id"])
        print("sql语句:"+sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        conn.cursor().execute(sql)
        result=conn.commit()
        conn.close()
        print("result结果为:",result)     
        self.write("")  

class selectHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_select_get方法了")

        #print("challenges:",dir(challenges))
      
        self.render("fileserver/templates/select.html"
        	
        	#,impedes=impedes
        	#,challenges=challenges
        	
        	)
        
    def post(self):
        print("进入fileserver_select_post方法了")
        #print("post数据:"+self.get_argument(status"))
        sql="select * from file where 1=1 "
        if self.get_argument("keyword","空值")!="空值":
            sql=sql+" and (name like '%"+self.get_argument("keyword")+"%')"
        if self.get_argument("address","空值")!="空值":
            sql=sql+" and (address like '%"+self.get_argument("address")+"%')"

        print("sql is:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        files=conn.cursor().execute(sql)
        result=conn.commit()


        print("files is:",files)
        #print("data is:",data)
        self.render("fileserver/templates/result.html"
        		,files=files)


class detailHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入filehouse_select_get方法了")
        sql="select * from file where id = "+self.get_argument("id")
        file=common.find("baigaopeng_fileserver",sql)
        self.render("fileserver/templates/detail.html"
        	,file=file
        	)
        
    def post(self):
        print("进入warehouse_select_post方法了")
        #print("post数据:"+self.get_argument(status"))
        sql="select * from file where 1=1 "
        if self.get_argument("keyword","空值")!="空值":
            sql=sql+" and (name like '%"+self.get_argument("keyword")+"%')"
        if self.get_argument("address","空值")!="空值":
            sql=sql+" and (address like '%"+self.get_argument("address")+"%')"
        print("sql is:",sql)
        conn=sqlite3.connect("projects3/db/baigaopeng_fileserver.db")
        files=conn.cursor().execute(sql)
        result=conn.commit()
        

        print("files is:",files)
        #print("data is:",data)
        self.render("fileserver/templates/result.html"
        		,files=files)

class listsHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_lists")
        #访问统计
        common.tongji("fileserver_lists")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            
            # sql="select * from file"
            # files = common.select("organization",sql)
            # for vo in files:
            #     if "fileserver_upload" in vo["filepath"]:
            #         vo["filepath"] = "File/upload"+vo["filepath"][17:]
            #         print("修改后：",vo["filepath"])
            #         sql="update file set filepath = '"+vo["filepath"]+"' where id ="+str(vo["id"])
            #         result=common.execute("organization",sql)
            #         if result==False:
            #             break


            sql="select * from file where access_level='public'"
            files=common.select("organization",sql)
            print("files:",files)
            if files[0]["id"] is None:
                files[0]={'id': 0, 'easy_memorize_name': "", 'uid': self.get_argument("uid"), 'filepath': "", 'download_number': 0, 'ctime': 0, 'confirmed': "",'liyonglv':0}
            else:
                for vo in files:
                    vo["liyonglv"]=int(vo["download_number"]/((time.time()-vo["ctime"])/86400)*10000)
            self.render(os.path.join(common.BASE_DIR,"organization","templates","File","lists.html")
                        ,files=files
                        )

class listHandler(tornado.web.RequestHandler):
    def get(self):
        #两部分组成，一个是自己的文件，另一个是分享的文件（包括自己分享的）
        print("进入fileserver_lists")
        #访问统计
        common.tongji("fileserver_lists")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            sql="select * from file where uid = "+self.get_argument("uid")+" order by access_level asc,download_number / ((strftime('%s','now') - ctime)/86400.0 +1 ) desc"
            myself_files=common.select("organization",sql)
            #print("myself_files:",myself_files)
            if myself_files[0]["id"] is None:
                myself_files[0]={'id': 0, 'easy_memorize_name': "", 'uid': self.get_argument("uid"), 'filepath': "", 'download_number': 0, 'ctime': 0, 'confirmed': "",'access_level':'public'}
            
            
            sql1="select * from file where access_level = 'public' order by download_number / ((strftime('%s','now') - ctime)/86400.0+1) desc"
            share_files=common.select("organization",sql1)#别人共享的文件
            #print("share_files:",share_files)
            if share_files[0]["id"] is None:
                share_files[0]={'id': 0, 'easy_memorize_name': "", 'uid': self.get_argument("uid"), 'filepath': "", 'download_number': 0, 'ctime': 0, 'confirmed': "",'access_level':'public'}
        
            # #增加对分卷压缩文件的文件名进行处理的功能，解决因为文件名增加了随机数之后不能自动解压的问题。实现方式就是检测出是分卷压缩文件时删除其中的随机数。后来想到可以将此功能扩展到所有文件，文件唯一性交给用户自行负责。服务器上添加随机数的目的只是为了防止服务器上存储的文件被同名文件覆盖
            # share_files = [{**item,'filepath':f"File/upload/{item['filepath'][10:]}"} for item in share_files]
            # myself_files = [{**item,'filepath':f"File/upload/{item['filepath'][10:]}"} for item in myself_files]
            


            self.render(os.path.join(common.BASE_DIR,"organization","templates","File","list.html")
                        ,myself_files=myself_files
                        ,share_files=share_files
                        )

# class listHandler(tornado.web.RequestHandler):
#     async def get(self):
#         try:
#             print("进入fileserver_lists")
#             common.tongji("fileserver_lists")
            
#             # 检查用户登录状态
#             if not self.get_cookie("user_id"):
#                 print("没有cookie")
#                 # 使用render方法而不是手动设置头信息
#                 self.render(
#                     os.path.join(common.BASE_DIR, "organization", "templates", "Index", "login.html"),
#                     message="没有登录或者已经登录过期，请登录"
#                 )
#                 return
            
#             # 安全获取uid参数
#             uid = self.get_argument("uid")
#             if not uid.isdigit():
#                 raise ValueError("无效的用户ID")
            
#             # 使用参数化查询防止SQL注入
#             sql = """
#                 SELECT * FROM file 
#                 WHERE uid = %s 
#                 ORDER BY access_level ASC, 
#                        download_number / ((strftime('%s','now') - ctime)/86400.0 + 1) DESC
#             """
#             myself_files = common.select("organization", sql, (uid,))
            
#             # 处理空结果
#             if not myself_files or myself_files[0].get("id") is None:
#                 myself_files = [{
#                     'id': 0, 
#                     'easy_memorize_name': "", 
#                     'uid': uid, 
#                     'filepath': "", 
#                     'download_number': 0, 
#                     'ctime': 0, 
#                     'confirmed': "",
#                     'access_level': 'public'
#                 }]
            
#             # 获取共享文件
#             sql_share = """
#                 SELECT * FROM file 
#                 WHERE access_level = 'public' 
#                 ORDER BY download_number / ((strftime('%s','now') - ctime)/86400.0 + 1) DESC
#             """
#             share_files = common.select("organization", sql_share)
            
#             if not share_files or share_files[0].get("id") is None:
#                 share_files = [{
#                     'id': 0, 
#                     'easy_memorize_name': "", 
#                     'uid': uid, 
#                     'filepath': "", 
#                     'download_number': 0, 
#                     'ctime': 0, 
#                     'confirmed': "",
#                     'access_level': 'public'
#                 }]
            
#             # 直接使用render方法，让Tornado自动处理头信息
#             self.render(
#                 os.path.join(common.BASE_DIR, "organization", "templates", "File", "list.html"),
#                 myself_files=myself_files,
#                 share_files=share_files
#             )
            
#         except Exception as e:
#             # 在异常处理中也要使用render方法
#             self.set_status(500)
#             self.render(
#                 os.path.join(common.BASE_DIR, "organization", "templates", "Error", "error.html"),
#                 error_message=str(e)
#             )


# class listHandler(tornado.web.RequestHandler):
#     async def get(self):
#         try:
#             print("进入fileserver_lists")
#             common.tongji("fileserver_lists")
            
#             # 检查用户登录状态
#             if not self.get_cookie("user_id"):
#                 print("没有cookie")
#                 # 明确设置 Content-Type 和 Content-Length
#                 response = "没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>"
#                 self.set_header("Content-Type", "text/html; charset=utf-8")
#                 self.set_header("Content-Length", str(len(response)))
#                 self.write(response)
#                 return
            
#             # 安全获取uid参数
#             uid = self.get_argument("uid")
#             if not uid.isdigit():
#                 raise ValueError("无效的用户ID")
            
#             # 使用参数化查询防止SQL注入
#             sql = """
#                 SELECT * FROM file 
#                 WHERE uid = %s 
#                 ORDER BY access_level ASC, 
#                        download_number / ((strftime('%s','now') - ctime)/86400.0 + 1) DESC
#             """
#             myself_files = common.select("organization", sql, (uid,))
            
#             # 处理空结果
#             if not myself_files or myself_files[0].get("id") is None:
#                 myself_files = [{
#                     'id': 0, 
#                     'easy_memorize_name': "", 
#                     'uid': uid, 
#                     'filepath': "", 
#                     'download_number': 0, 
#                     'ctime': 0, 
#                     'confirmed': "",
#                     'access_level': 'public'
#                 }]
            
#             # 获取共享文件
#             sql_share = """
#                 SELECT * FROM file 
#                 WHERE access_level = 'public' 
#                 ORDER BY download_number / ((strftime('%s','now') - ctime)/86400.0 + 1) DESC
#             """
#             share_files = common.select("organization", sql_share)
            
#             if not share_files or share_files[0].get("id") is None:
#                 share_files = [{
#                     'id': 0, 
#                     'easy_memorize_name': "", 
#                     'uid': uid, 
#                     'filepath': "", 
#                     'download_number': 0, 
#                     'ctime': 0, 
#                     'confirmed': "",
#                     'access_level': 'public'
#                 }]
            
#             # 准备模板路径
#             template_path = os.path.join(
#                 common.BASE_DIR, 
#                 "organization", 
#                 "templates", 
#                 "File", 
#                 "list.html"
#             )
            
#             # 手动设置响应头
#             self.set_header("Content-Type", "text/html; charset=utf-8")
            
#             # 渲染模板
#             html = self.render_string(
#                 template_path,
#                 myself_files=myself_files,
#                 share_files=share_files
#             )
            
#             # 确保 Content-Length 是字符串
#             self.set_header("Content-Length", str(len(html)))
#             self.write(html)
#             await self.finish()
            
#         except Exception as e:
#             self.set_status(500)
#             error_msg = f"发生错误: {str(e)}"
#             self.set_header("Content-Type", "text/html; charset=utf-8")
#             self.set_header("Content-Length", str(len(error_msg)))
#             self.write(error_msg)
#             await self.finish()

# class downloadHandler(tornado.web.RequestHandler):
      
#     async def get(self):
#         tornado.web.RequestHandler._convert_header_value = lambda self, value: value  # 禁用头部校验
#         sql="select * from file where id="+self.get_argument("id")
#         file=common.find("organization",sql)
#         #下载量加1
#         sql="update file set download_number=download_number+1 where id="+self.get_argument("id")
#         result=common.execute("organization",sql)
#         if not result:
#             self.write("<html><head></head><body><script>window.alert('更新下载量出错，请联系白老师！')</script></body></html>")


#         self.set_header('Content-Type', 'application/octet-stream')
#         # #去掉文件名中前十位的日期标签
#         if file['id']>=911:
#             file_path=file['filepath'][10:]
#         else:
#             file_path = file["filepath"]
        
#         # file_path=file["filepath"][10:]

#         self.set_header("Content-Disposition","attachment; filename*=UTF-8 "+file_path)
#         # # 4. RFC标准编码响应头
#         # encoded_name = quote(display_name, safe='')
#         # self.set_header("Content-Type", "application/octet-stream")
#         # self.set_header("Content-Disposition", 
#         #     f"attachment; filename*=UTF-8''{encoded_name}")     
#         from urllib.parse import quote   
#         filename=os.path.basename(file_path)
#         print("filename",filename)
#         self.set_header("Content-Type", "application/octet-stream")
#         encoded_name = quote(os.path.basename(file_path), safe='')  # RFC 6266编码
#         self.set_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")      

        
#         # 流式分块传输（内存占用恒定）
#         chunk_size = 1024 * 1024  # 1MB/块
#         with open(os.path.join(common.BASE_DIR,"organization","templates", "File","upload",file["filepath"]), "rb") as f:
#             while True:
#                 chunk = f.read(chunk_size)
#                 if not chunk: 
#                     break
#                 self.write(chunk)
#                 await self.flush()  # 关键：非阻塞发送[6](@ref)


# class downloadHandler(tornado.web.RequestHandler):
#     async def get(self):
#         try:
#             # 你原有的下载逻辑完全保持不变
#             tornado.web.RequestHandler._convert_header_value = lambda self, value: value
#             sql = "select * from file where id=" + self.get_argument("id")
#             file = common.find("organization", sql)
#             sql = "update file set download_number=download_number+1 where id=" + self.get_argument("id")
#             result = common.execute("organization", sql)
#             if not result:
#                 self.write("<html><head></head><body><script>window.alert('更新下载量出错，请联系白老师！')</script></body></html>")

#             self.set_header('Content-Type', 'application/octet-stream')
#             if file['id'] >= 911:
#                 file_path = file['filepath'][10:]
#             else:
#                 file_path = file["filepath"]

#             self.set_header("Content-Disposition", "attachment; filename*=UTF-8 " + file_path)
#             from urllib.parse import quote
#             filename = os.path.basename(file_path)
#             print("filename", filename)
#             self.set_header("Content-Type", "application/octet-stream")
#             encoded_name = quote(os.path.basename(file_path), safe='')
#             self.set_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")

#             # 流式传输部分：添加StreamClosedError捕获
#             chunk_size = 1024 * 1024
#             with open(os.path.join(common.BASE_DIR, "organization", "templates", "File", "upload", file["filepath"]), "rb") as f:
#                 while True:
#                     chunk = f.read(chunk_size)
#                     if not chunk:
#                         break
#                     try:
#                         self.write(chunk)
#                         await self.flush()  # 非阻塞发送
#                     except tornado.iostream.StreamClosedError:
#                         # 客户端在下载过程中断开了连接（如取消下载），直接退出循环
#                         logging.warning("Client stream closed during download.")
#                         return  # 关键：立即返回，避免后续操作

#         except Exception as e:
#             # 捕获任何未预期的异常，记录并返回错误信息
#             logging.error(f"Download error: {e}")
#             self.set_status(500)
#             self.finish("Internal server error during download.")

class downloadHandler(tornado.web.RequestHandler):
    async def get(self):
        try:
            file_id = self.get_argument("id")
            sql = "select * from file where id=" + file_id
            file = common.find("organization", sql)
            
            # 检查文件记录是否存在
            if not file:
                self.set_status(404)
                self.write("Error: File record not found in database.")
                await self.finish()
                return
            
            # 下载量加1
            sql = "update file set download_number=download_number+1 where id=" + file_id
            result = common.execute("organization", sql)
            if not result:
                logging.warning(f"Failed to update download count for file ID: {file_id}")
                # 这里选择记录警告但继续下载流程，不中断

            # 确定文件路径
            if file['id'] >= 911:
                file_path = file['filepath'][10:]
            else:
                file_path = file["filepath"]
            
            # 构建文件的绝对路径
            absolute_file_path = os.path.join(common.BASE_DIR, "organization", "templates", "File", "upload", file["filepath"])
            
            # 检查文件是否真实存在于磁盘上
            if not os.path.isfile(absolute_file_path):
                self.set_status(404)
                self.write("Error: The file was not found on the server.")
                await self.finish()
                return

            # 设置响应头
            self.set_header('Content-Type', 'application/octet-stream')
            from urllib.parse import quote
            encoded_name = quote(os.path.basename(file_path), safe='')
            self.set_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")

            # 流式传输文件内容
            chunk_size = 1024 * 1024  # 1MB/块
            with open(absolute_file_path, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break  # 文件读取完毕
                    try:
                        self.write(chunk)
                        await self.flush()  # 非阻塞发送
                    except tornado.iostream.StreamClosedError:
                        # 客户端提前关闭了连接（如取消下载）
                        logging.info("Client closed connection during download.")
                        return  # 直接返回，不再继续发送
            # self.finish() 会在异步方法结束时自动调用

        except Exception as e:
            logging.error(f"Unexpected error in download: {e}")
            if not self._finished:
                self.set_status(500)
                self.write("An internal server error occurred during download.")
                self.finish()


# class BaseHandler(tornado.web.RequestHandler):
#     def write_error(self, status_code, **kwargs):
#         # 1. 清除可能已存在的响应缓冲区，避免重复写入
#         if self._write_buffer:
#             self.clear()

#         # 2. 设置一个简单且安全的错误信息体
#         #    确保 Content-Length 是字符串
#         message = f"HTTP Error {status_code}"
#         self.set_header("Content-Type", "text/plain")
#         self.set_header("Content-Length", str(len(message))) # 关键：确保是str

#         # 3. 如果是 500 错误，可以记录日志，方便调试
#         if status_code == 500:
#             self.application.settings.get("logger", logging).error(
#                 "Uncaught exception in write_error", exc_info=kwargs.get("exc_info")
#             )

#         # 4. 写入错误信息并完成响应
#         self.write(message)
#         self.finish()

# # 让你的 downloadHandler 继承自 BaseHandler
# class downloadHandler(BaseHandler):

#     async def get(self):
#         try:
#             # ... 你的数据库查询和下载量更新逻辑 ...

#             file_id = self.get_argument("id")
#             # 建议：使用参数化查询防止SQL注入，例如使用 %s 占位符和单独传递参数
#             # sql = "select * from file where id = %s"
#             # file = common.find("organization", sql, (file_id,))

#             file_path = os.path.join(common.BASE_DIR, "organization", "templates", "File", "upload", file["filepath"])

#             # !!! 关键：在设置任何 headers 之前检查文件是否存在 !!!
#             if not os.path.isfile(file_path):
#                 raise tornado.web.HTTPError(404, f"File not found: {file_path}")

#             # 只有在确认文件存在后，才设置下载相关的 headers
#             self.set_header('Content-Type', 'application/octet-stream')
#             encoded_name = quote(os.path.basename(file_path), safe='')
#             self.set_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")

#             chunk_size = 1024 * 1024
#             with open(file_path, "rb") as f:
#                 while True:
#                     chunk = f.read(chunk_size)
#                     if not chunk:
#                         break
#                     self.write(chunk)
#                     try:
#                         # 添加异常捕获，防止网络连接中途断开导致 flush 出错
#                         await self.flush()
#                     except tornado.iostream.StreamClosedError:
#                         # 客户端提前关闭了连接，记录日志并优雅退出循环
#                         logging.warning("Client closed connection during download.")
#                         break
#             # self.finish() 会被自动调用，因为方法是 async 的

#         except tornado.web.HTTPError:
#             # 重新抛出已知的HTTP错误，让 write_error 处理
#             raise
#         except Exception as e:
#             # 捕获其他所有未知异常，记录并返回500
#             logging.error(f"Unexpected error in download: {e}", exc_info=True)
#             raise tornado.web.HTTPError(500, "Internal server error occurred during download.")
    
# import logging # 确保导入logging模块
# import os
# from urllib.parse import quote
# import tornado.web
# import tornado.ioloop

# class downloadHandler(tornado.web.RequestHandler):
#     async def get(self):
#         try:
#             file_id = self.get_argument("id")
#             # 1. 从数据库获取文件信息
#             # 强烈建议使用参数化查询以防止SQL注入，例如：
#             # sql = "SELECT * FROM file WHERE id = %s"
#             # file = common.find("organization", sql, (file_id,))
#             sql = "SELECT * FROM file WHERE id=" + file_id
#             file = common.find("organization", sql)

#             # 2. 检查文件记录是否存在
#             if not file: # 如果file为None或空字典
#                 raise tornado.web.HTTPError(404, f"File with ID {file_id} not found in database.")

#             # 3. 更新下载量 (可选，同样建议参数化查询)
#             sql_update = "UPDATE file SET download_number = download_number + 1 WHERE id=" + file_id
#             result = common.execute("organization", sql_update)
#             if not result:
#                 # 更新下载量失败，记录警告但通常不中断下载
#                 logging.warning("Failed to update download count for file ID: %s", file_id)

#             # 4. 构建文件绝对路径
#             # 根据你的项目结构调整路径拼接
#             if file['id'] >= 911:
#                 relative_path = file['filepath'][10:]
#             else:
#                 relative_path = file["filepath"]
#             file_path = os.path.join(common.BASE_DIR, "organization", "templates", "File", "upload", relative_path)

#             # 5. 检查文件是否真实存在于磁盘上
#             if not os.path.isfile(file_path):
#                 raise tornado.web.HTTPError(404, f"File not found on server: {os.path.basename(file_path)}")

#             # 6. 设置响应头，指示文件下载
#             self.set_header('Content-Type', 'application/octet-stream')
#             encoded_name = quote(os.path.basename(relative_path), safe='')
#             self.set_header("Content-Disposition", f"attachment; filename*=UTF-8''{encoded_name}")

#             # 7. 流式传输文件内容
#             chunk_size = 1024 * 1024 # 1MB
#             with open(file_path, 'rb') as f:
#                 while True:
#                     chunk = f.read(chunk_size)
#                     if not chunk:
#                         break # 文件读取完毕
#                     try:
#                         self.write(chunk)
#                         await self.flush() # 分块发送
#                     except tornado.iostream.StreamClosedError:
#                         # 客户端提前关闭了连接（如下载取消）
#                         logging.warning("Client stream closed early during download of file ID: %s", file_id)
#                         return # 直接返回，不再继续发送
#             # self.finish() 会在方法结束时自动调用

#         except tornado.web.HTTPError:
#             # 重新抛出我们已知的HTTP错误，让write_error处理
#             raise
#         except Exception as e:
#             # 捕获其他所有未知异常，记录日志并返回500错误
#             logging.error("Unexpected error during download: %s", e, exc_info=True)
#             raise tornado.web.HTTPError(500, "Internal server error occurred during download.")

#     def write_error(self, status_code, **kwargs):
#         # 清除可能已存在的缓冲区
#         if self._write_buffer:
#             self.clear()
#         # 设置错误信息内容
#         message = f"HTTP Error {status_code}"
#         if status_code == 404:
#             message = "The requested resource was not found."
#         elif status_code == 500:
#             message = "An internal server error occurred."
#         # 确保Content-Length是字符串类型
#         self.set_header("Content-Type", "text/plain")
#         self.set_header("Content-Length", str(len(message)))
#         self.write(message)
#         self.finish()

class setPublicHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_lists")
        #访问统计
        common.tongji("fileserver_lists")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            sql="update file set access_level= 'public' where id ="+self.get_argument("id")
            result=common.execute("organization",sql)
            if result==False:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("系统出错，请联系老师！");</script></body></html>') 
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");</script></body></html>') 
            

class setPrivateHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_lists")
        #访问统计
        common.tongji("fileserver_lists")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:
            sql="update file set access_level= 'private' where id ="+self.get_argument("id")
            result=common.execute("organization",sql)
            if result==False:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("系统出错，请联系老师！");</script></body></html>') 
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("修改成功！");</script></body></html>') 


# class changeFilePathHandler(tornado.web.RequestHandler):
#     def get(self):
#         print("进入fileserver_lists")
#         #访问统计
#         #common.tongji("fileserver_lists")
#         sql = "select * from file"
#         files = common.select("organization",sql)
#         for vo in files:
#             if "fileserver_upload" in vo["filepath"]:
#                 sql = "update file set filepath = 'File/upload"+vo["filepath"][17:]+ "' where id="+str(vo["id"])
#                 print(sql)
#                 result = common.execute("organization",sql)
                
class changeFilePathHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入fileserver_lists")
        #访问统计
        #common.tongji("fileserver_lists")
        sql = "select * from file"
        files = common.select("organization",sql)
        for vo in files:
                sql = "update file set filepath = 'upl"+vo["filepath"]+ "' where id="+str(vo["id"])
                print(sql)
                result = common.execute("organization",sql)
                
                                