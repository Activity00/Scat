# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/5 13:57
"""
from sqlalchemy import create_engine

engin = create_engine('sqlite:///:memory:', echo=True)
