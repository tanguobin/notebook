#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from orm.user import UserModel

class UserCtrl(object):

    def __init__(self):
        self.user = UserModel()

    def __getattr__(self, name):
        return getattr(self.user, name)
