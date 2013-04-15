#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import logging
from handler.base import BaseHandler
from control import ctrl

logger = logging.getLogger(__name__)

class CategoryHandler(BaseHandler):
    def get(self):
        result,code = {},'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        cid = self.get_argument('cid', '')
        p = self.get_argument('p', 0)
        psize = self.get_argument('psize', 20)
        if cid:
            notes = ctrl.note.get_all_note(uid=u['uid'],cid=cid)
            total = len(notes)
            notelist = []
            for note in notes:
                notelist.append({
                    'nid':note.id,
                    'title':note.title,
                    'time':note.uptime.strftime('%Y-%m-%d %H:%M:%S')
                })
            result = {
                'total': total,
                'notelist': notelist
            }
        else:
            cates = ctrl.note.get_category(uid=u['uid'])
            total = len(cates)
            catelist = []
            for cate in cates:
                count = ctrl.note.get_note_count(uid=u['uid'],cid=cate.id)
                catelist.append({'cid':cate.id,'name':cate.name,'count':count})
            result = {
                'total': total,
                'catelist': catelist
            }
        self.send_json(result, code)

class NotebookHandler(BaseHandler):
    def get(self):
        result,code = {},'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        try:
            nid = self.get_argument('nid')
            note = ctrl.note.get_note_detail(nid)
            images,title,content = [],'',''
            if note:
                images = note.images.split('|')
                title = note.title
                content = note.content
            result = {
                'title': title,
                'content': content,
                'images': images
            }
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_PARAM'
        self.send_json(result, code)

class UpdateNoteHandler(BaseHandler):
    def post(self):
        result,code = {},'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        try:
            nid = self.get_argument('nid','')
            cid = self.get_argument('cid')
            title = self.get_argument('title','')
            content = self.get_argument('content','')
            if nid:
                ctrl.note.update_note(id=nid,uid=u['uid'],cid=cid,title=title,content=content)
                note = ctrl.note.get_note_detail(nid)
                if note:
                    result = {
                        'success': 1,
                        'time': note.uptime.strftime('%Y-%m-%d %H:%M:%S')
                    }
            else:
                note = ctrl.note.add_notebook(u['uid'],cid,title,content)
                result = {
                    'success': 1,
                    'nid': note.id,
                    'time': note.uptime.strftime('%Y-%m-%d %H:%M:%S')
                }
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_PARAM'
            result = {
                'success': 0
            }
        self.send_json(result, code)

class UpdateCateHandler(BaseHandler):
    pass

class RemoveHandler(BaseHandler):
    def get(self):
        result,code = {},'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        nid = self.get_argument('nid','')
        cid = self.get_argument('cid','')
        if not nid and not cid:
            code = 'E_PARAM'
            self.send_json(result, code)
            return
        try:
            if nid:
                ctrl.note.delete_note(id=nid)
            if cid:
                ctrl.note.delete_note(cid=cid)
            result = {
                'success': 1
            }
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_INTER'
            result = {
                'success': 0
            }
        self.send_json(result, code)

class ImageHandler(BaseHandler):
    pass
