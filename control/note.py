#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from orm.note import NoteModel

class NoteCtrl(object):

    def __init__(self):
        self.note = NoteModel()

    def __getattr__(self, name):
        return getattr(self.note, name)
