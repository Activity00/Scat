# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 14:30
"""
import importlib
import os

from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.web import Application, RequestHandler

from scat.distributed.node import RemoteObject
from scat.server.connection import NetConnection
from scat.server.globalobject import GlobalObject
from scat.server.handler.net_handler import WebSocketNetHandler, NetHandler
from scat.server.netserver import NetServer

setting_str = os.environ.get('SCAT_SETTINGS_MODULE', None)
if not setting_str:
    raise Exception
settings = importlib.import_module(setting_str)

class MyHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write('xxoo')


class ScatServer:
    """ it can be used for single server """
    def __init__(self, server_name):
        self.server_name = server_name
        self.remote = {}

    def config(self):
        """
        config the server based server name, scat will be found the basic config
        from settings.SERVERS.
        """
        if not self.server_name or self.server_name not in settings.SERVERS:
            raise Exception('server name ({}) not found'.format(self.server_name))

        server_config = settings.SERVERS[self.server_name]
        master_config = settings.MASTER
        net_port = server_config.get('net_port')
        web_port = server_config.get('web_port')
        app = server_config.get('app')
        romote_list = server_config.get('remote_list', [])  # remote node list

        if net_port:
            net_protocol = server_config.get('net_protocol', 'tcp')
            if net_protocol == 'websocket':
                net = WebSocketNetHandler
                app = Application(r'.*$', [('/', net)])
                server = HTTPServer(app)
                server.listen(net_port)
            elif net_protocol == 'socketio':
                # TODO socketio protocol implement
                net = None
            else:
                net = NetHandler()
                server = NetServer(net)
                server.listen(net_port)

            GlobalObject().net = net

        if web_port:
            web_root = Application()  # web use a application contains handler
            http_server = HTTPServer(web_root)
            http_server.listen(web_port)
            GlobalObject().web_root = web_root

        if master_config:
            pass

        if app:
            importlib.import_module(app)
            if web_port:
                GlobalObject().web_root.add_handlers(r'.*$', GlobalObject().web_handlers)

        for cnf in romote_list:
            # self.remote[cnf.get('root_name')] = RemoteObject(self.server_name)
            pass

    def start(self):
        self.config()
        ioloop.IOLoop.current().start()

if __name__ == '__main__':
    pass
