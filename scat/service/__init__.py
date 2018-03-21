# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/4 18:29
"""
from scat.server import GlobalObject


web_root = GlobalObject().web_root
GlobalObject().web_handlers = []


def web_service(cls):
    GlobalObject().web_handlers.append((r'/{}/'.format(cls.__name__.lower()), cls))

