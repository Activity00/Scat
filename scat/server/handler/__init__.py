# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 18:40
"""
from tornado.web import Application
from scat import ScatObject


def root_handler(cls):
    pass


def net_handler(cls):
    net = ScatObject.net
    if isinstance(net, Application):
        for k, v in cls.__dict__.items():
            if not k.startswith('_'):
                setattr(net, k, v)
    else:
        for k, v in cls.__dict__.items():
            if not k.startswith('_'):
                setattr(net, k, v)

