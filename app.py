#-*-coding:utf8;-*-
#app.py


import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient



import organization.FileController
import organization.IndexController
import organization.UserController
import organization.WorksController
import organization.PublicityController
import organization.ExamController
import organization.NoteController
import organization.RecordController
import organization.CompetitionController
import organization_admin.FileController
import organization_admin.IndexController
import organization_admin.QuestionController
import organization_admin.ResolutionController
import organization_admin.CompetitionController
import organization_admin.SigninController
import organization_admin.RecordController
import organization_admin.ExamController
import organization_admin.SigninController


from tornado.options import define, options
import myportal.common as common
import config
import organization.ResolutionController
import organization_admin.UserController
import jobs.auto_record_audio as auto_record_audio
import jobs.scheduler as scheduler
from tornado.web import StaticFileHandler
define("port", default=9000, help="run on the given port", type=int)

#tornado.web.RequestHandler._convert_header_value = lambda self, value: value  # 禁用头部校验

if __name__ == '__main__':
    tornado.options.parse_command_line()
    # 初始化定时任务（一行搞定）
    scheduler.init_scheduler()
    
    app = tornado.web.Application(
        handlers=[
            (r'/organization', organization.IndexController.loginHandler)
        , (r'/', organization.IndexController.loginHandler)
        , (r'/organization/File/list', organization.FileController.listHandler)
        , (r'/organization/File/lists', organization.FileController.listsHandler)
        , (r'/organization/File/add', organization.FileController.addHandler)
        , (r'/organization/File/del', organization.FileController.delHandler)
        , (r'/organization/File/setPublic', organization.FileController.setPublicHandler)
        , (r'/organization/File/setPrivate', organization.FileController.setPrivateHandler)   
        , (r'/organization/File/change', organization.FileController.changeFilePathHandler)        
        , (r'/organization/File/download', organization.FileController.downloadHandler)  
        , (r'/organization/Resolution/lists', organization.ResolutionController.listsHandler)   
        , (r'/organization/User/lists', organization.UserController.listsHandler)      
        , (r'/organization/User/check_pass', organization.UserController.checkPassHandler)
        , (r'/organization/Works/lists', organization.WorksController.listsHandler)   
        , (r'/organization/Works/add', organization.WorksController.addHandler)        
        , (r'/organization/Works/detail', organization.WorksController.detailHandler)     
        , (r'/organization/Note/list', organization.NoteController.listHandler)
        , (r'/organization/Note/edit', organization.NoteController.editHandler)
        , (r'/organization/Note/add', organization.NoteController.addHandler)
        , (r'/organization/Note/image_upload', organization.NoteController.imageUploadHandler)
        , (r'/organization/Note/detail', organization.NoteController.detailHandler)
        , (r'/organization/Note/add_collection', organization.NoteController.addCollectionHandler)
        , (r'/organization/Note/collection_list', organization.NoteController.collectionListHandler)
        , (r'/organization/Note/del_collection', organization.NoteController.delCollectionHandler)
        , (r'/organization/Publicity/index', organization.PublicityController.indexHandler)  
        , (r'/organization/Index/register', organization.IndexController.registerHandler)
        , (r'/organization/Index/login', organization.IndexController.loginHandler)
        , (r'/organization/Index/click_statistics', organization.IndexController.clickStatisticsHandler)
        , (r'/organization/Exam/select_module', organization.ExamController.selectModuleHandler)
        , (r'/organization/Exam/select_difficult', organization.ExamController.selectDifficultHandler)
        , (r'/organization/Exam/index', organization.ExamController.indexHandler)
        , (r'/organization/Record/lists', organization.RecordController.listsHandler)
        , (r'/organization_admin/Record/lists', organization_admin.RecordController.listsHandler)
        , (r'/organization_admin/Record/add', organization_admin.RecordController.addHandler)
        , (r'/organization/Competition/lists', organization.CompetitionController.listsHandler)
        , (r'/organization/Competition/join', organization.CompetitionController.joinHandler)
        , (r'/organization_admin/Question/add', organization_admin.QuestionController.addHandler)
        , (r'/organization_admin/Question/detail', organization_admin.QuestionController.detailHandler)
        , (r'/organization_admin/Question/lists', organization_admin.QuestionController.listsHandler)
        , (r'/organization_admin/Question/operation_add', organization_admin.QuestionController.operationAddHandler)
        , (r'/organization_admin/Question/edit', organization_admin.QuestionController.editHandler)
        , (r'/organization_admin', organization_admin.IndexController.indexHandler)
        , (r'/organization_admin/User/lists', organization_admin.UserController.listsHandler)
        , (r'/organization_admin/Index/click_statistics', organization_admin.SigninController.listsHandler)
        , (r'/organization_admin/User/check_pass', organization_admin.UserController.checkPassHandler)
        , (r'/organization_admin/Index/signin_manager', organization_admin.IndexController.signinManagerHandler)
        , (r'/organization_admin/Index/add_expected_signin', organization_admin.SigninController.addExpectedSigninHandler)
        , (r'/organization_admin/Index/signin_history', organization_admin.SigninController.listHandler)
        , (r'/organization_admin/Index/index', organization_admin.IndexController.indexHandler)
        , (r'/organization_admin/User/edit', organization_admin.UserController.editHandler)
        , (r'/organization_admin/File/lists', organization_admin.FileController.listsHandler)
        , (r'/organization_admin/File/del', organization_admin.FileController.delHandler)
        , (r'/organization_admin/File/download', organization_admin.FileController.downloadHandler)
        , (r'/organization_admin/Exam/lists', organization_admin.ExamController.listsHandler)        
        , (r'/organization_admin/Exam/add_question', organization_admin.ExamController.addQuestionHandler)        
        , (r'/organization_admin/Resolution/lists', organization_admin.ResolutionController.listsHandler)
        , (r'/organization_admin/Resolution/add', organization_admin.ResolutionController.addHandler)
        , (r'/organization_admin/Competition/lists', organization_admin.CompetitionController.listsHandler)
        , (r'/organization_admin/Competition/add', organization_admin.CompetitionController.addHandler)
        , (r'/organization/Competition/detail', organization.CompetitionController.detailHandler)     
        , (r'/organization_admin/Signin/expected_signin_time_lists', organization_admin.SigninController.expectedSigninlistsHandler)    
        , (r'/organization_admin/Competition/edit', organization_admin.CompetitionController.editHandler)           
        #静态资源路由
        # ,(r'/static_jobs_recordings/(.*)', StaticFileHandler, {'path': config.get_path("jobs","recordings")})
        ,(r'/static_single_choice_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","single_choice")})
        ,(r'/static_multiple_choice_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","multiple_choice")})
        ,(r'/static_fill_blank_question_images/(.*)', StaticFileHandler, {'path': config.get_path("sangao","Question","images","fill_blank")})


        ],
        template_path=os.path.join(os.path.dirname(__file__), ""),
        static_path=os.path.join(os.path.dirname(__file__), ""),  # 启用静态文件服务
        # static_url_prefix="/organization/static/",        
        autoreload=True,
        compiled_template_cache=False,
        # 允许最大 5GB 请求体
        max_buffer_size=5 * 1024 * 1024 * 1024,  # 5GB
    )

    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()




