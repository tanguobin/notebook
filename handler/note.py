#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import logging
import hashlib
from handler.base import BaseHandler
from control import ctrl

logger = logging.getLogger(__name__)

class CategoryHandler(BaseHandler):
    def get(self):
        result,code = [],'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        cid = self.get_argument('cid', '')
        if cid:
            notes = ctrl.note.get_all_note(uid=u['uid'],cid=cid)
            notelist = []
            for note in notes:
                notelist.append({
                    'nid':note.id,
                    'title':note.title,
                    'time':note.uptime.strftime('%Y-%m-%d %H:%M:%S')
                })
            result = notelist
        else:
            cates = ctrl.note.get_category(uid=u['uid'])
            catelist = []
            for cate in cates:
                count = ctrl.note.get_note_count(uid=u['uid'],cid=cate.id)
                catelist.append({'cid':cate.id,'name':cate.name,'count':count})
            result = catelist
        self.send_json(result, code)

class NotebookHandler(BaseHandler):
    def get(self):
        result,code = [],'E_OK'
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
                images = [self.application.settings['static_host']+image for image in note.images.split('&') if image]
                title = note.title
                content = note.content
            result = [{
                'title': title,
                'content': content,
                'images': images
            }]
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_PARAM'
        self.send_json(result, code)

class UpdateNoteHandler(BaseHandler):
    def post(self):
        result,code = [],'E_OK'
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
            cate = ctrl.note.get_category(cid=cid)
            if not cate:
                code = 'E_RESRC'
                self.send_json(result,code)
                return
            if nid:
                ctrl.note.update_note(id=nid,uid=u['uid'],cid=cid,title=title,content=content)
                note = ctrl.note.get_note_detail(nid)
                if note:
                    result = [{
                        'time': note.uptime.strftime('%Y-%m-%d %H:%M:%S')
                    }]
            else:
		note = ctrl.note.get_notebook(u['uid'],cid,title)
		if not note:
                    note = ctrl.note.add_notebook(u['uid'],cid,title,content)
                    result = [{
                        'nid': note.id,
                        'time': note.uptime.strftime('%Y-%m-%d %H:%M:%S')
                    }]
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_PARAM'
        self.send_json(result, code)

class UpdateCateHandler(BaseHandler):
    def post(self):
        result,code = [],'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        cid = self.get_argument('cid','')
        name = self.get_argument('name','')
        if not name:
            code = 'E_PARAM'
            self.send_json(result, code)
            return
        try:
            if cid:
                ctrl.note.update_category(id=cid,uid=u['uid'],name=name)
                result = [{
                    'cid': cid
                }]
            else:
		category = ctrl.note.get_category(uid=u['uid'],name=name)
		if not category:
                    category = ctrl.note.add_category(uid=u['uid'],names=[name])[0]
                    result = [{
                        'cid': category.id
                    }]
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_INTER'
        self.send_json(result, code)

class RemoveHandler(BaseHandler):
    def get(self):
        result,code = [],'E_OK'
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
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_INTER'
        self.send_json(result, code)

class ImageHandler(BaseHandler):
    def post(self):
        result,code = [],'E_OK'
        u = self.current_user
        if not u:
            code = 'E_AUTH'
            self.send_json(result, code)
            return
        try:
            nid = int(self.get_argument('nid'))
            all_files = self.request.files['file']
            urllist = []
            for upload_file in all_files:
                md5_sign = hashlib.md5(upload_file['body'])
                sign = md5_sign.hexdigest() + '.jpg'
                static_path = self.application.settings['static_path']
                file_path = '/'.join([static_path, sign])
                fopen = open(file_path, 'wb')
                fopen.write(upload_file['body'])
                fopen.close()
                urllist.append(sign)
            result = [{
                'url': urllist
            }]
            images = '&'.join(urllist)
            if images:
                ctrl.note.update_note(id=nid,images=images)
        except Exception,e:
            logger.exception("%s\n%s\n", self.request, e)
            code = 'E_INTER'
        self.send_json(result, code)
