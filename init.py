#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import os
import sys
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.autoreload import add_reload_hook
from tornado.options import define, options

define("port", default=8000, help="run on this port", type=int)
define("debug", default=True, help="enable debug mode")
define('project_path', default=sys.path[0], help='deploy_path')

tornado.options.parse_command_line()

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'static_path': os.path.join(options.project_path, 'static'),
            'xsrf_cookies': False,
            'debug': options.debug,
            'gzip': True,
            'static_host': 'http://api1.enote.ctyun.cn/static/',
        }
        tornado.web.Application.__init__(self, [
            (r'/login/oauth_redirect', 'handler.user.LoginHandler'),
            (r'/logout', 'handler.user.LogoutHandler'),
            (r'/usercheck', 'handler.user.UserHandler'),
            (r'/category', 'handler.note.CategoryHandler'),
            (r'/notebook', 'handler.note.NotebookHandler'),
            (r'/updatenote', 'handler.note.UpdateNoteHandler'),
            (r'/updatecate', 'handler.note.UpdateCateHandler'),
            (r'/rm', 'handler.note.RemoveHandler'),
            (r'/upload', 'handler.note.ImageHandler'),
            (r'/.*', 'handler.base.BaseHandler'),
        ], **settings)

def free_resource():
    from orm import orm
    orm.close()

if __name__ == "__main__":
    add_reload_hook(free_resource)
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
