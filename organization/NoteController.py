import tornado
import sqlite3

import warnings
warnings.filterwarnings('ignore')
import time
import myportal.common as common
import os
import uuid #生成唯一的随机码（何为唯一，不知道如何实现的，可能和时间戳相关才能在不存储的前提下保证唯一吧）
import re #正则

class indexHandler(tornado.web.RequestHandler):
    def get(self):
        #统计模块开始
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_myportal.db")
        sql="insert into click(click_time,click_action) values("+str(int(time.time()))+",'task_index')"
        result=conn.cursor().execute(sql)
        conn.commit()
        conn.close()
        #统计模块结束
        sql="select * from note where status='未处理'"
        conn=sqlite3.connect("D:\\projects3\\db\\sangao.db")
        tasks=conn.cursor().execute(sql)
        result=conn.commit()
        self.render("sangao\\templates\\Note\\result.html"
        		,tasks=tasks)
        self.render("sangao\\templates\\Note\\result.html")

class listHandler(tornado.web.RequestHandler):
    def get(self):
        #此函数被复用
        # print("参数：",self.get_argument("collection_id"))
        if self.get_argument("collection_id",None)!=None:
            sql="select * from note where user_id="+self.get_argument("user_id")+" and collection_id="+self.get_argument("collection_id")
            
            my_notes=common.select("organization",sql)
            self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","list.html"),my_collection_notes=my_notes)
        else:
            #有两部分组成，一个是自己的笔记，另一个是分享的笔记(包括自己的),两部分有重合，但不影响。相反，在两部分中都能找到自己的笔记，说明分享成功了
            sql="select * from note where user_id="+self.get_argument("user_id")
            my_notes=common.select("organization",sql)
            sql="select * from note where access_level='public'"
            share_notes=common.select("organization",sql)
        
            self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","list.html"),my_notes=my_notes,share_notes=share_notes)

#和list的区别在于，list是自己的笔记列表，lists是所有人的笔记列表
class listsHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from note where collection="+self.get_argument("collection") + " and user_id = "+self.get_argument("user_id")
        notes=common.select("organization",sql)


        self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","lists.html"),notes=notes)




class addHandler(tornado.web.RequestHandler):
    def get(self):
        print("进入note_add")
        common.tongji("note_add")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:        
            #合集模型
            sql="select * from collection where user_id="+self.get_cookie("user_id")
            my_collections=common.select("organization",sql)

            self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","add.html"),user_id=self.get_cookie("user_id"),my_collections=my_collections)
    def post(self):
            data={}
            #content的处理,由于content中很可能有双引号，单引号这些sql的关键符号，而这些都是在sql语句中是无法正常被执行，需要做特殊处理，比如单引号需要用两个单引号进行转义
            data["content"] = self.get_argument("content").replace("'","''")
            data["title"] = self.get_argument("title")
            data["access_level"] = self.get_argument("access_level")
            data["user_id"] = self.get_argument("uid")
            data["collection_id"]=self.get_argument("collection")
            sql= "insert into note(title,content,access_level,user_id,collection_id) values('"+data["title"]+"','"+data["content"]+"','"+data["access_level"]+"',"+data["user_id"]+","+data["collection_id"]+")"
            #print("sql:",sql)
            result=common.execute("organization",sql)
            if result:
                user_id=data["user_id"]
                self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('修改成功！');window.location.href = 'list?user_id="+str(data["user_id"])+"';</script></body></html>") 
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("系统出错，请联系白老师！");</script></body></html>') 




class editHandler(tornado.web.RequestHandler):
    def get(self):
        print("note_edit")
        #访问统计
        common.tongji("note_edit")
        if self.get_cookie("user_id",None) ==None:#如果没有cookie就去登录
            print("没有cookie")
            self.write("没有登录或者已经登录过期，请点击<a href='/organization/Index/login'>登录</a>")
            #self.render(os.path.join(common.BASE_DIR,"organization","templates","Index","login.html"))
        else:             
            # sql="select note.id as note_id,note.collection_id,note.user_id,note.title,note.content,note.access_level,collection.name as collection from note join collection on note.collection_id=collection.id where note_id = "+self.get_argument("id")
            # note=common.find("organization",sql)
            #联合查询有可能会没有结果，所以不如改为分体查询
            sql="select * from note where id="+self.get_argument("id")
            note=common.find("organization",sql)

            #接着看一下此note在collection中是否建有合集
            sql="select * from collection where id="+str(note["collection_id"])
            collection=common.find("organization",sql)
            #下面取出collections，配合前端select元素使用
            if collection!=None:
                sql="select * from collection where user_id="+str(note["user_id"])+" and id!="+str(note["collection_id"])
            else:
                sql="select * from collection where user_id="+str(note["user_id"])
            collections = common.select("organization",sql)

            self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","edit.html"),note=note,collections=collections,collection=collection)
        
    def post(self):
   
            data={}
            #content的处理,由于content中很可能有双引号，单引号这些sql的关键符号，而这些都是在sql语句中是无法正常被执行，需要做特殊处理，比如单引号需要用两个单引号进行转义
            data["content"] = self.get_argument("content").replace("'","''")
            data["title"] = self.get_argument("title")
            data["access_level"] = self.get_argument("access_level")
            data["collection"] = self.get_argument("collection")
            sql="update note set content='"+data["content"]+"',title='"+data["title"]+"',collection_id='"+data["collection"]+"',access_level='"+data["access_level"]+"' where id="+self.get_argument("id")
            print("sql:",sql)
            result=common.execute("organization",sql)
            if result:
                sql="select * from note where id = "+self.get_argument("id")
                note=common.find("organization",sql)
                
                self.write("<html><head><title>提醒</title></head><body><script type='text/javascript'>window.alert('修改成功！');window.location.href = 'list?user_id="+str(note["user_id"])+"';</script></body></html>") 
            else:
                self.write('<html><head><title>提醒</title></head><body><script type="text/javascript">window.alert("系统出错，请联系白老师！");</script></body></html>') 



class selectHandler(tornado.web.RequestHandler):
    def get(self):
        #print("进入task_select_get方法了")

        impedes=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from impede where status = 'abled'")
        challenges=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db").cursor().execute("select * from challenge C where status='abled' order by (select count(*) from task T where T.challenge=C.name) desc")
        #print("challenges:",dir(challenges))
      
        self.render("sangao\\templates\\Note\\select.html"
        	
        	,impedes=impedes
        	,challenges=challenges
        	
        	)
        
    def post(self):
        #print("进入task_select_post方法了")
        #print("post数据:"+self.get_argument(status"))
        sql="select * from task where 1=1 "
        if self.get_argument("status","空值")!="空值":
            sql=sql+" and (status like '%"+self.get_argument("status")+"%')"
        if self.get_argument("impede","空值")!="空值":
            sql=sql+" and (impede like '%"+self.get_argument("impede")+"%')"
        if len(self.get_arguments("address[]","空值"))>0:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[0]+"%') "
        if len(self.get_arguments("address[]","空值"))>1:
            sql=sql+" and (address like '%"+self.get_arguments("address[]")[1]+"%')"
        if self.get_argument("keyword","空值")!="空值":
            sql=sql+" and (title like '%"+self.get_argument("keyword")+"%' or \
        	 content like '%"+self.get_argument("keyword")+"%' or \
        	 id like '%"+self.get_argument("keyword")+"%' \
        	)"
        if self.get_argument("keyword2","nullvalue")!="nullvalue":
            sql=sql+" and (title like '%"+self.get_argument("keyword2")+"%' or \
        		content like '%"+self.get_argument("keyword2")+"%' or \
        		id like '%"+self.get_argument("keyword2")+"%' \
        		)"
        		
        if len(self.get_arguments("type[]","nullvalue"))>0:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[0]+"%'")
        if len(self.get_arguments("type[]","nullvalue"))>1:
            sql=sql+(" and type like '%"+self.get_arguments("type[]")[1]+"%'")
        if self.get_argument("challenge","nullvalue")!="nullvalue":
            sql=sql+(" and challenge like '%"+self.get_argument("challenge")+"%'")
        sql=sql+" order by id asc"
        #print("sql is:",sql)
        conn=sqlite3.connect("D:\\projects3\\db\\baigaopeng_task.db")
        tasks=conn.cursor().execute(sql)
        result=conn.commit()
        self.render("sangao\\templates\\Note\\result.html"
        		,tasks=tasks)


class detailHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from note where id="+self.get_argument("id")
        note= common.find("organization",sql)
        #print("content",note["content"])
        #取出此笔记所属合集，为何要分开查询而不是用联合查询，主要是因为此笔记有可能没有属于合集，那样的话联合查询就空，还要再去查询一遍笔记条目
        sql="select * from collection where id="+str(note["collection_id"])
        #print("sql:",sql)
        result=common.find("organization",sql)
        #print("result:",result)
        if result==None:
            collection="无"
        else:
            collection=result["name"]
        self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","detail.html"),note=note,collection=collection)
        
class imageUploadHandler(tornado.web.RequestHandler):
    def post(self):
        # file = self.request.files['imgFile'][0]  # KindEditor固定参数名
        # filename = secure_filename(file['filename'])
        # save_path = os.path.join("uploads", filename)
        # with open(save_path, 'wb') as f:
        #     f.write(file['body'])
        # self.write({"error": 0, "url": f"/static/uploads/{filename}"})  # 必须返回JSON格式[6](@ref)
        file_format=self.get_argument("dir")
        if file_format=="image":
            try:
                file = self.request.files["imgFile"][0] # KindEditor固定参数名
                filename = file["filename"]
            #将request缓存中的文件写入本地磁盘前有如下如下几个处理模块，可以根据自己情况选择并进行组合使用
                # 1. 安全文件名处理（原生实现）
                # safe_name = self._secure_filename(filename)
                # if not safe_name:
                #     return self.write({"error": 1, "message": "无效文件名"})
                
                # 2. 文件类型校验
                # if not self._is_valid_image(file['content_type']):
                #     return self.write({"error": 1, "message": "仅支持JPG/PNG/GIF图片"})
                
                # 3. 生成唯一文件名
                file_ext = os.path.splitext(filename)[1]
                unique_name = f"{uuid.uuid4().hex}{file_ext}"
                
                #创建上传目录
                upload_dir = "organization/organization/templates/Note/upload"
                os.makedirs(upload_dir, exist_ok=True)
                
                #保存文件
                save_path = os.path.join(upload_dir, unique_name)
                with open(save_path, 'wb') as f:
                    f.write(file['body'])

                # 返回KindEditor标准响应
                self.write({
                    "error": 0,
                    "url": self.static_url(f"organization/Templates/Note/upload/{unique_name}") 
                })                    
            except Exception as e:
                self.write({"error": 1, "message": f"服务器错误: {str(e)}"})


    
    def _secure_filename(self, filename):
        """原生安全文件名处理"""
        # 剥离路径信息
        name = os.path.basename(filename)
        # 保留扩展名
        _, ext = os.path.splitext(name)
        # 移除特殊字符
        clean_name = re.sub(r'[^\w\-.]', '', name)
        return clean_name if clean_name and ext else None
    
    def _is_valid_image(self, content_type):
        """原生图片类型校验"""
        valid_types = {
            'image/jpeg': '.jpg',
            'image/png': '.png',
            'image/gif': '.gif'
        }
        return content_type in valid_types
    

class addCollectionHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","add_collection.html"),user_id=self.get_argument("user_id"))


    def post(self):
        data={}
        user_id=data["user_id"]=self.get_argument("user_id")
        data["ctime"]=str(int(time.time()))
        data["name"]=self.get_argument("collection")
        sql = "insert into collection(user_id,name,ctime) values("+data["user_id"]+",'"+data["name"]+"',"+data["ctime"]+")"
        print("sql:",sql)
        result=common.execute("organization",sql)
        
        if result:
            self.write(
                '''
                <html><head><script>
                window.alert("添加成功！");
                window.location.href("list?user_id=user_id");
                </script></head></html>
                '''
                )
        else:
            self.write(
                '''
                <html><head><script>
                window.alert("添加失败，请联系白老师！");
                window.location.href("list?user_id=user_id");
                </script></head></html>
                '''
            )


class collectionListHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from collection where user_id="+self.get_argument("user_id")
        my_collections=common.select("organization",sql)

        self.render(os.path.join(common.BASE_DIR,"organization","templates","Note","collection_list.html"),my_collections=my_collections)

class delCollectionHandler(tornado.web.RequestHandler):
    def get(self):
        sql="select * from note where collection_id ="+self.get_argument("collection_id")+ " and user_id="+self.get_argument("user_id")
        belong_collection_notes=common.select("organization",sql)
        print("笔记数：",belong_collection_notes)
        if len(belong_collection_notes)==None:
            sql="delete from collection where collection_id="+self.get_argument("collection_id")
            result=common.execute("organization",sql)
            if result:
                self.write(
                    '''
                <html><head><script>
                window.alert("删除成功！");
                </script></head></html>
'''
                )
            else:
                self.write(
                    '''
                    <html><head><script>
                    window.alert("删除数据出错，请联系白老师！");
                    </script></head></html>
                    '''
                )                
        else:
            self.write(
                '''
                <html><head><script>
                window.alert("此合集下还有笔记，不能删除，请先将笔记删除或者转至其他合集！");
                </script></head></html>
                '''
            )                            
        sql="select * from collection where user_id="+self.get_argument("user_id")
        my_collections=common.select("organization",sql)
        self.redirect(os.path.join(common.BASE_DIR,"organization","templates","Note","collection_list.html")+"?user_id="+self.get_argument("user_id"))