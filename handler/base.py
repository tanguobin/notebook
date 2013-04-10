#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import json
import datetime
import tornado.web

class BaseHandler(tornado.web.RequestHandler):

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
