# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/21 15:49
"""
from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.web import Application

from scat.rpc.server.handlers import JsonRPCHandler


class Tree:
    def power(self, base, power, modulo=None):
        return pow(base, power, modulo)

    def _private(self):
        # Wont be callable
        return False


class MyHandler(JsonRPCHandler):
    tree = Tree()

    def add(self, x, y):
        return x + y

    def echo(self, obj):
        return obj


if __name__ == '__main__':
    app = Application(handlers=[(r'/RPC2', MyHandler)])
    server = HTTPServer(app)
    server.listen(8000)
    ioloop.IOLoop.current().start()