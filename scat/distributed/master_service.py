# coding: utf-8

"""
@author: 武明辉 
@time: 2018/3/24 15:37
"""
from scat import ScatObject
from scat.service import web_service


@web_service
class Stop:
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('stop')


@web_service
class Reload:
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('reload')

