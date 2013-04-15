#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set et sw=4 ts=4 sts=4 ff=unix fenc=utf8:

import sys
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('/'.join([sys.path[0], 'conf', 'settings.conf']))
