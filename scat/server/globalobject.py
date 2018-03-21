# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 12:53
"""
from scat.utils.singleton import Singleton


class GlobalObject(metaclass=Singleton):
    def __init__(self):
        self.root = None
        self.web_root = None
        self.remote = {}
        self.net = None

