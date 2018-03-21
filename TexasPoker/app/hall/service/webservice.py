# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/10 19:37
"""
import tornado.web

from scat.service import web_service


@web_service
class Stop(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('mlgb')

