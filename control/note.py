#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from orm.note import NoteModel

class NoteCtrl(object):

    def __init__(self, ctrl):
        self.note = NoteModel()
        self.cache = ctrl.cache

    def __getattr__(self, name):
        return getattr(self.note, name)

    def get_all_note(self, uid=None, cid=None):
        key = 'allnote_%s_%s' % (uid, cid)
        r = self.cache.get(key)
        if not r:
            r = self.note.get_all_note(uid, cid)
            self.cache.set(key, r)
        return r

    def get_category(self, uid=None, name=None, cid=None):
        key = 'category_%s_%s_%s' % (uid, name, cid)
        r = self.cache.get(key)	
        if not r:
            r = self.note.get_category(uid, name, cid)
            self.cache.set(key, r)
        return r

    def get_note_count(self, uid=None, cid=None):
        key = 'notecount_%s_%s' % (uid, cid)
        r = self.cache.get(key)
        if not r:
            r = self.note.get_note_count(uid, cid)
            self.cache.set(key, r)
        return r

    def get_note_detail(self, nid=None):
        key = 'notedetail_%s' % (nid)
        r = self.cache.get(key)
        if not r:
            r = self.note.get_note_detail(nid)
            self.cache.set(key, r)
        return r

    def update_note(self, id=None, uid=None, cid=None, title=None, content=None, images=None):
        ctrl.note.update_note(id=id,uid=uid,cid=cid,title=title,content=content,images=images)
        self.cache.delete('allnote_%s_%s' % (uid, cid))
        self.cache.delete('notedetail_%s' % (id))

    def get_notebook(self, uid=None, cid=None, title=None):
        key = 'notebook_%s' % (uid, cid, title)
        r = self.cache.get(key)
        if not r:
            r = self.note.get_notebook(uid,cid,title)
            self.cache.set(key, r)
        return r

    def add_notebook(self, uid=None, cid=None, title=None, content=None):
        self.note.add_notebook(uid,cid,title,content)
        self.cache.delete('notecount_%s_%s' % (uid, cid))
        self.cache.delete('allnote_%s_%s' % (uid, cid))

    def update_category(self, id=None, uid=None, name=None):
        self.note.update_category(id,uid,name)
        self.cache.delete('category_%s_%s_%s' % (uid, name, id))

    def add_category(self, uid=None, names=None):
        self.note.add_category(uid,names)
        self.cache.delete('category_%s_%s_%s' % (uid, None, None))

    def delete_note(self, id=None, cid=None):
        if id:
            self.note.delete_note(id)
            self.cache.delete('notedetail_%s' % (id))
        if cid:
            self.note.delete_note(cid)
            self.cache.delete('category_%s_%s_%s' % (None, None, cid))
