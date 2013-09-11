#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import pylibmc

from conf import config
from control.note import NoteCtrl
from control.user import UserCtrl

class Ctrl(object):

    def __init__(self):
        session_server = config.get('SESSION','server')
        cache_server = config.get('CACHE','server')
        behaviors = {'tcp_nodelay':True,'ketama':True}
        self.session = pylibmc.Client(eval(session_server),binary=True,behaviors=behaviors)
        self.cache = pylibmc.Client(eval(cache_server),binary=True,behaviors=behaviors)
        self.user = UserCtrl(self)
        self.note = NoteCtrl(self)

    @staticmethod
    def instance():
        name = 'singleton'
        if not hasattr(Ctrl, name):
            setattr(Ctrl, name, Ctrl())
        return getattr(Ctrl, name)

ctrl = Ctrl.instance()
