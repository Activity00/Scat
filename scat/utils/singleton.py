# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 12:52
"""


class Singleton(type):
    """Singleton Metaclass"""
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]