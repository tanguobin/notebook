#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TIMESTAMP, VARCHAR, TEXT
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import UniqueConstraint
from orm import Base, orm

class Notebook(Base):

    # column
    id = Column(INTEGER, primary_key=True)
    uid = Column(INTEGER, nullable=False, server_default='0', index=True)
    cid = Column(INTEGER, nullable=False, server_default='0', index=True) # Category id
    title = Column(VARCHAR(32), nullable=False, server_default='')
    content = Column(TEXT, nullable=False)
    images = Column(VARCHAR(255), nullable=False, server_default='')
    creatime = Column(DATETIME, nullable=False, default=func.now())
    uptime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint('uid', 'cid', 'title', name='uid_cid_title'),
            Base.__table_args__
        )

class Category(Base):

    # column
    id = Column(INTEGER, primary_key=True)
    uid = Column(INTEGER, nullable=False, server_default='0', index=True)
    name = Column(VARCHAR(64), nullable=False, server_default='')
    creatime = Column(DATETIME, nullable=False, default=func.now())
    uptime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint('uid', 'name', name='uid_name'),
            Base.__table_args__
        )

class NoteModel(object):

    def __init__(self):
        Base.metadata.create_all(orm.engine)
        self.session = orm.session

    def delete_note(self,id=None,cid=None):
        if id:
            return self.session.query(Notebook).filter(Notebook.id==id).delete()
        if cid:
            return self.session.query(Notebook).filter(Notebook.cid==cid).delete()
        self.session.commit()
        return True

    def add_notebook(self,uid=None,cid=None,title=None,content=None):
        note = Notebook(uid=uid,cid=cid,title=title,content=content)
        self.session.add(note)
        self.session.commit()
        return note

    def update_note(self,id=None,**args):
        mapping = {
            'uid': Notebook.uid,
            'cid': Notebook.cid,
            'title': Notebook.title,
            'content': Notebook.content,
            'images': Notebook.images
        }
        attr = {}
        for k in args:
            attr[mapping[k]] = args[k]
        self.session.query(Notebook).filter(Notebook.id==id).update(attr)
        self.session.commit()
        return True

    def update_category(self,id=None,**args):
        mapping = {
            'id': Category.id,
            'uid': Category.uid,
            'name': Category.name
        }
        attr = {}
        for k in args:
            attr[mapping[k]] = args[k]
        self.session.query(Category).filter(Category.id==id).update(attr)
        self.session.commit()
        return True

    def add_category(self,uid=None,names=None):
        '''
        batch adding category
        '''
        catelist = []
        for name in names:
            cate = Category(uid=uid,name=name)
            self.session.add(cate)
            catelist.append(cate)
        self.session.commit()
        return catelist

    def get_category(self,uid=None):
        '''
        get user all category
        '''
        return self.session.query(Category).filter(Category.uid==uid).all()

    def get_note_detail(self,nid=None):
        '''
        get notebook detail
        '''
        return self.session.query(Notebook).filter(Notebook.id==nid).limit(1).scalar()

    def get_all_note(self,uid=None,cid=None):
        '''
        get user's notebook by uid and cid
        '''
        return self.session.query(Notebook).filter(Notebook.uid==uid,Notebook.cid==cid).all()

    def get_note_count(self,uid=None,cid=None):
        '''
        get user's notebook count
        '''
        return self.session.query(Notebook).filter(Notebook.uid==uid,Notebook.cid==cid).count()
