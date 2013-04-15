#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from tornado.ioloop import PeriodicCallback

from conf import config

class SubCls(object):

    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8'
    }

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=SubCls)

class ORM(object):

    def __init__(self):
        host = config.get('DB_NOTE', 'host')
        port = config.get('DB_NOTE', 'port')
        user = config.get('DB_NOTE', 'user')
        db = config.get('DB_NOTE', 'db')
        passwd = config.get('DB_NOTE', 'passwd')

        mysql = 'mysql://%s:%s@%s:%s/%s?charset=utf8'%(user,passwd,host,port,db)
        self.engine = create_engine(mysql,echo=True)
        print '--->init db:%s' % mysql
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.ping()
        PeriodicCallback(self.ping, 3600*1000).start()

    def ping(self):
        self.session.execute('set names utf8')
        self.session.execute('set autocommit=1')

    def __del__(self):
        self.close()

    def close(self):
        if self.engine:
            self.engine.dispose()
        if self.session:
            self.session.close()

    @staticmethod
    def instance():
        name = 'singleton'
        if not hasattr(ORM, name):
            setattr(ORM, name, ORM())
        return getattr(ORM, name)

# global
orm = ORM.instance()
