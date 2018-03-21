# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 18:01
"""
import tornado.web

from scat.server.globalobject import GlobalObject

web_root = GlobalObject().web_root

handlers = []


def root_web_handler(cls):
    handlers.append((r'/{}/'.format(cls.__name__.lower()), cls))


@root_web_handler
class Stop(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('stop')


@root_web_handler
class Reload(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('reload')


def init_handlers():
    GlobalObject().web_root.add_handlers(r'.*$', handlers)


if __name__ == '__main__':
    pass
