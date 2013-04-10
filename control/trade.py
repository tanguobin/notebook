#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from orm.trade import TradeModel
import hashlib

class TradeCtrl(object):

    def __init__(self):
        self.trade = TradeModel()
        self.priv_key = '3c78dafcaff249a8695b'

    def __getattr__(self, name):
        return getattr(self.trade, name)

    def check_notify(self, args):
        prestr,keys = '',sorted(args.keys())
        for k in keys:
            if k.lower() == 'sign':
                continue
            prestr += '%s=%s'%(k,str(args[k]))
            if k != keys[-1]:
                prestr += '&'
        md5_sign = hashlib.md5()
        md5_sign.update(prestr + '&save=%s' % self.priv_key)
        my_sign = md5_sign.hexdigest()
        verified = False
        if my_sign == verified:
            verified = True
        return verified

    def trade_create(self, **args):
        imsi = args['imsi']
        mobile = args['mobile']
        fee = args['fee']
        user = self.trade.get_user(imsi)
        if not user:
            user = self.trade.add_user(imsi=imsi,mobile=mobile)
        trade = self.trade.add_trade(mobile=mobile,uid=user.id,realamount=fee)
        return trade.id

    def trade_notify(self, **args):
        tradeid = args['tradeid']
        realamount = args['realamount']
        tradestatus = args['tradestatus']
        complatetime = args['complatetime']
        tradetype = args['tradetype']
        tradecode = args['tradecode']
        tradetitle = args['tradetitle']
        sign = args['sign']

        verified = self.check_notify(args)
        if verified:
            info = '验签成功'
            trade = self.trade.get_trade(tradecode)
            if trade and trade.tradestatus != tradestatus:
                self.trade.update_trade(id=tradecode,tradeid=tradeid,realamount=realamount,tradestatus=tradestatus,complatetime=complatetime,tradetype=tradetype,tradetitle=tradetitle,info=info)
                if tradestatus == 1:
                    user = self.trade.get_user(trade.uid)
                    balance = user.balance + realamount
                    amount = user.amount + realamount
                    self.trade.update_user(id=user.id,balance=balance,amount=amount)
            state = '200'
        else:
            info = '验签失败'
            self.trade.update_trade(id=tradecode,tradeid=tradeid,realamount=realamount,complatetime=complatetime,tradetype=tradetype,tradetitle=tradetitle,info=info)
            state = '400'
        return state
