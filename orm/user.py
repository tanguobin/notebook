#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from sqlalchemy import Column, text, Index
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TIMESTAMP, VARCHAR, BIGINT
from sqlalchemy.sql.expression import func
from sqlalchemy.ext.declarative import declared_attr
from orm import Base, orm

class SnsBind(Base):

    # column
    id = Column(INTEGER, primary_key=True)
    uid = Column(INTEGER, nullable=False, server_default='0')
    siteid = Column(VARCHAR(16), nullable=False, server_default='')
    sid = Column(BIGINT, nullable=False, server_default='0')
    name = Column(VARCHAR(64), nullable=False, server_default='')
    nick = Column(VARCHAR(64), nullable=False, server_default='')
    email = Column(VARCHAR(64), nullable=False, server_default='')
    avatar = Column(VARCHAR(255), nullable=False, server_default='')
    access_token = Column(VARCHAR(64), nullable=False, server_default='')
    access_secret = Column(VARCHAR(64), nullable=False, server_default='')
    expires = Column(BIGINT, nullable=False, server_default='0')
    creatime = Column(DATETIME, nullable=False, default=func.now())
    uptime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

    @declared_attr
    def __table_args__(cls):
        return (
            Index('sid_siteid', 'sid', 'siteid'),
            Base.__table_args__
        )

class User(Base):

    # column
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(64), nullable=False, server_default='')
    email = Column(VARCHAR(64), nullable=False, server_default='')
    creatime = Column(DATETIME, nullable=False, default=func.now())
    uptime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class UserModel(object):

    def __init__(self):
        Base.metadata.create_all(orm.engine)
        self.session = orm.session

    def add_snsbind(self,uid=None,siteid='189',sid=None,name=None,nick=None,email=None,avatar=None,access_token=None,access_secret=None,expires=None):
        snsbind = SnsBind(uid=uid,siteid=siteid,sid=sid,name=name,nick=nick,email=email,avatar=avatar,access_token=access_token,access_secret=access_secret,expires=expires)
        self.session.add(snsbind)
        self.session.commit()
        return True

    def add_user(self,name=None,email=None):
        user = User(name=name,email=email)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self,id):
        return self.session.query(User).filter(User.id==id).limit(1).scalar()

    def get_sns(self, sid, siteid='189'):
        return self.session.query(SnsBind).filter(SnsBind.sid==sid,SnsBind.siteid==siteid).limit(1).scalar()

    def update_user(self,id=None,**args):
        mapping = {
            'name': User.name,
            'email': User.email
        }
        attr = {}
        for k in args:
            attr[mapping[k]] = args[k]
        self.session.query(User).filter(User.id==id).update(attr)
        self.session.commit()
        return True
