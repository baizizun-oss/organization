# -*-coding:utf8;-*-
# qpy:console


import os.path

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import time
import random
import http.client
import json
import sqlite3
from datetime import datetime

import myportal.common as common







class indexHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","login.html"))    

    def post(self):
        if self.get_argument("username")=="bgp1984" and self.get_argument("password")=="founder#021665":
            self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","index.html"))    
        else:
            self.write("账号密码错误！")

            
class signinManagerHandler(tornado.web.RequestHandler):

    def get(self):
        self.render(os.path.join(common.BASE_DIR,"organization_admin","templates","signin_manager.html"))    
