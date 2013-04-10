#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

from control.trade import TradeCtrl

class Ctrl(object):

    def __init__(self):
        self.trade = TradeCtrl()

    @staticmethod
    def instance():
        name = 'singleton'
        if not hasattr(Ctrl, name):
            setattr(Ctrl, name, Ctrl())
        return getattr(Ctrl, name)

ctrl = Ctrl.instance()
