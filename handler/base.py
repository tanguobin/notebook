#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import json
import uuid
import time
import hashlib
import datetime
import tornado.web

from control import ctrl
from conf import config

class BaseHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('welcome to 189 notebook')

    def parse_module(self, module):
        _module,_sub = '',''
        if module:
            arr = module.split('/')
            if len(arr) >= 3:
                _module = arr[1]
                _sub = arr[2]
            elif len(arr) >= 2:
                _module = arr[1]
        return '%s__%s'%(_module,_sub) if _sub else _module

    def jsondump(self, data):
        date2str = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None
        res = json.dumps(data, default=date2str)
        self.write(res)

    def send_json(self, result, code):
        err_desc = eval(config.get('DESC', 'err_desc'))
        code_desc = eval(config.get('DESC', 'code_desc'))
        r = {"status": {"code": code_desc[code], "msg": err_desc[code]}, "result": result}
        self.jsondump(r)

    def gen_session_id(self, secret):
        return hashlib.sha1("%s%s%s" % (uuid.uuid4(), time.time(), secret)).hexdigest()

    def get_session_id(self, expires=0):
        cookie_name = config.get('SESSION', 'cookie_name')
        secret = config.get('SESSION', 'secret')
        if expires:
            expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires)
        session_id = self.gen_session_id(secret)
        self.set_cookie(cookie_name, session_id, expires=expires)
        return session_id

    def get_session(self):
        '''
        get session
        '''
        cookie_name = config.get('SESSION', 'cookie_name')
        session_id = self.get_cookie(cookie_name)
        session = ctrl.session.get(str(session_id))
        return session

    def delete_session(self):
        '''
        delete session
        '''
        cookie_name = config.get('SESSION', 'cookie_name')
        session_id = self.get_cookie(cookie_name)
        if session_id:
            ctrl.session.delete(session_id)
        self.clear_cookie(cookie_name)

    def get_current_user(self):
        return self.get_session()
