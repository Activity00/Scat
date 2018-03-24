# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 14:30
"""
from twisted.internet.error import ReactorAlreadyInstalledError
import tornado.platform.twisted
try:
    tornado.platform.twisted.install()
except ReactorAlreadyInstalledError:
    pass
from twisted.internet import reactor

import importlib
import os

from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.web import Application

from scat.distributed.node import RemoteObject
from scat.distributed.root import PBRoot, BilateralFactory
from scat.server.connection import NetConnection
from scat.server.globalobject import GlobalObject
from scat.server.handler.net_handler import WebSocketNetHandler, NetHandler
from scat.server.netserver import NetServer
from scat.service import Service

setting_str = os.environ.get('SCAT_SETTINGS_MODULE', None)
if not setting_str:
    raise Exception
settings = importlib.import_module(setting_str)


class ScatServer:
    """ it can be used for single server """
    def __init__(self, server_name):
        self.server_name = server_name
        self.master_remote = None   # master Node
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
        server = server_config.get('server')
        remote_list = server_config.get('remote_list', [])  # remote node list
        root_port = server_config.get('root_port')

        if root_port:
            root = PBRoot(Service("root_service"))
            reactor.listenTCP(root_port, BilateralFactory(root))

        if web_port:
            app = Application()
            http_server = HTTPServer(app)
            http_server.listen(web_port)
            GlobalObject().web_root = app

        if net_port:
            net = NetHandler()
            server = NetServer(net)
            server.listen(net_port)
            GlobalObject().net = net

        if master_config:
            master_port = master_config.get('root_port')
            master_host = master_config.get('root_host')
            self.master_remote = RemoteObject(self.server_name)
            addr = ('localhost', master_port) if not master_host else (master_host, master_port)
            self.master_remote.connect(addr)
            GlobalObject().master_remote = self.master_remote

        if server:
            importlib.import_module(server)

        for cnf in remote_list:
            # self.remote[cnf.get('root_name')] = RemoteObject(self.server_name)
            pass

    def start(self):
        self.config()
        print(self.server_name, 'stared')
        ioloop.IOLoop.current().start()

if __name__ == '__main__':
    pass