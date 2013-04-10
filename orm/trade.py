#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:
from sqlalchemy import Column, text
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.sql.expression import func
from orm import Base, orm

class Trade(Base):

    # column
    id = Column(INTEGER, primary_key=True)
    mobile = Column(VARCHAR(16), nullable=False, server_default='', index=True)
    uid = Column(INTEGER, nullable=False, server_default='0')
    tradeid = Column(INTEGER, nullable=False, server_default='0')
    realamount = Column(INTEGER, nullable=False, server_default='0')
    tradestatus = Column(INTEGER, nullable=False, server_default='0')
    complatetime = Column(DATETIME, nullable=False, server_default=text("'1970-01-01 00:00:00'"))
    tradetype = Column(VARCHAR(16), nullable=False, server_default='', index=True)
    tradetitle = Column(VARCHAR(64), nullable=False, server_default='')
    info = Column(VARCHAR(64), nullable=False, server_default='')
    creatime = Column(DATETIME, nullable=False, default=func.now())
    uptime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class User(Base):

    # column
    id = Column(INTEGER, primary_key=True)
    mobile = Column(VARCHAR(16), nullable=False, server_default='', index=True)
    imsi = Column(VARCHAR(32), nullable=False, server_default='', index=True)
    balance = Column(INTEGER, nullable=False, server_default='0')
    amount = Column(INTEGER, nullable=False, server_default='0')
    creatime = Column(DATETIME, nullable=False, default=func.now())
    uptime = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

class TradeModel(object):

    def __init__(self):
        Base.metadata.create_all(orm.engine)
        self.session = orm.session

    def add_trade(self,mobile=None,uid=None,tradeid=None,realamount=None,tradestatus=None,complatetime=None,tradetype=None,tradetitle=None,info=None):
        trade = Trade(mobile=mobile,uid=uid,tradeid=tradeid,realamount=realamount,tradestatus=tradestatus,complatetime=complatetime,tradetype=tradetype,tradetitle=tradetitle,info=info)
        self.session.add(trade)
        self.session.commit()
        return trade

    def add_user(self,mobile=None,imsi=None,balance=None,amount=None):
        user = User(mobile=mobile,imsi=imsi,balance=balance,amount=amount)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user(self,imsi):
        return self.session.query(User).filter(User.imsi==imsi).limit(1).scalar()

    def get_trade(self,id):
        return self.session.query(Trade).filter(Trade.id==id).limit(1).scalar()

    def update_trade(self,id=None,**args):
        mapping = {
            'mobile': Trade.mobile,
            'uid': Trade.uid,
            'tradeid': Trade.tradeid,
            'realamount': Trade.realamount,
            'tradestatus': Trade.tradestatus,
            'complatetime': Trade.complatetime,
            'tradetype': Trade.tradetype,
            'tradetitle': Trade.tradetitle,
            'info': Trade.info
        }
        attr = {}
        for k in args:
            attr[mapping[k]] = args[k]
        self.session.query(Trade).filter(Trade.id==id).update(attr)
        self.session.commit()
        return True

    def update_user(self,id=None,**args):
        mapping = {
            'mobile': Trade.mobile,
            'imsi': Trade.imsi,
            'balance': Trade.balance,
            'amount': Trade.amount
        }
        attr = {}
        for k in args:
            attr[mapping[k]] = args[k]
        self.session.query(User).filter(User.id==id).update(attr)
        self.session.commit()
        return True
