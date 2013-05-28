#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from handler.base import BaseHandler
from control import ctrl
from conf import config

class LoginHandler(BaseHandler):
    def get(self):
        u = self.current_user
        result, code = [], 'E_OK'
        if u:
            self.send_json(result, code)
            return
        res_code = int(self.get_argument('res_code'))
        res_message = self.get_argument('res_message')
        if res_code == 0 and res_message == 'Success':
            access_token = self.get_argument('access_token')
            open_id = int(self.get_argument('open_id'))
            expires_in = int(self.get_argument('expires_in'))
            sns = ctrl.user.get_sns(open_id)
            if sns:
                uid,uname = sns.uid,sns.name
            else:
                user = ctrl.user.add_user()
                uid,uname = user.id,user.name
                ctrl.user.add_snsbind(uid=uid,sid=open_id,access_token=access_token,expires=expires_in)
                ctrl.note.add_category(uid,names=['工作笔记','生活笔记','我的笔记'])
            session_id = self.get_session_id()
            ctrl.session.set(session_id, {'uid':uid,'siteid':'189','sid':open_id,'uname':uname}, expires_in)
        self.send_json(result, code)

class LogoutHandler(BaseHandler):
    def get(self):
        self.delete_session()

class UserHandler(BaseHandler):
    def get(self):
        u = self.current_user
        result, code = [], 'E_OK'
        if u:
            result = [{
                'isLogin': 1
            }]
        else:
            result = [{
                'isLogin': 0
            }]
            code = 'E_AUTH'
        self.send_json(result, code)
