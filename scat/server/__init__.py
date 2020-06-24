# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 14:30
"""
import asyncio

from twisted.internet.error import ReactorAlreadyInstalledError
import tornado.platform.twisted

from scat.db.cacheclient import CacheUtil
from scat.db.dbpool import DBPool
from scat.utils.logutil import ScatLog, set_file_handler

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
from scat.server.handler.net_handler import WebSocketNetHandler, NetHandler
from scat.server.netserver import NetServer
from scat.service import Service


class ScatServer:
    """ it can be used for single server """
    def __init__(self, server_name):
        self.server_name = server_name
        self.master_remote = None   # master Node
        self.remote = {}  # the dict this server connected to. {'server_name': ScatServer}
        self.remote_list = []

    def config(self):
        """
        config the server based server name, scat will be found the basic config
        from settings.SERVERS.
        """
        if not self.server_name or self.server_name not in settings.SERVERS:
            raise Exception('server name ({}) not found'.format(self.server_name))

        server_config = settings.SERVERS[self.server_name]
        master_config = settings.MASTER
        db_config = settings.DB
        cache_config = settings.CACHE

        net_port = server_config.get('net_port')
        web_port = server_config.get('web_port')
        self.remote_list = server_config.get('remote_list', [])  # remote node list
        root_port = server_config.get('root_port')
        app_config = server_config.get('app')
        log_path = server_config.get('log')
        support_db = server_config.get('db')
        support_cache = server_config.get('cache')
        reload_module = server_config.get('reload')

        if root_port:
            root = PBRoot(Service("root_service"))
            ScatObject.root = root
            reactor.listenTCP(root_port, BilateralFactory(root))

        if web_port:
            app = Application()
            http_server = HTTPServer(app)
            http_server.listen(web_port)
            ScatObject.web_root = app

        if net_port:
            net = NetHandler()
            server = NetServer(net)
            server.listen(net_port)
            ScatObject.net = net

        if log_path:
            set_file_handler(log_path)

        if support_db and db_config:
            logger.debug(str(db_config))
            DBPool.init_pool(**db_config)

        if support_cache and cache_config:
            host = cache_config.get('host')
            port = cache_config.get('port')
            # host_name = str(cache_config.get('host_name'))
            CacheUtil.init_pool(host, port)

        if reload_module:
            path_list = reload_module.split('.')
            ScatObject.reload_module = importlib.__import__(reload_module, fromlist=path_list[:1])

        for cnf in self.remote_list:
            name = cnf.get('root_name')
            self.remote[name] = RemoteObject(self.server_name)
        ScatObject.remote = self.remote

        ScatObject.remote_connect = self.remote_connect
        if not master_config:
            logger.warning('this node have no master config')
        else:
            master_port = master_config.get('root_port')
            master_host = master_config.get('root_host')
            self.master_remote = RemoteObject(self.server_name)
            addr = ('localhost', master_port) if not master_host else (master_host, master_port)
            self.master_remote.connect(addr)
            ScatObject.master_remote = self.master_remote

        importlib.import_module('scat.server.admin')

        if app_config:
            try:
                importlib.import_module(app_config + '.initialization')
            except ImportError:
                logger.warning('{} has no initialization.py so init will be ignore.'.format(self.server_name))

        try:
            importlib.import_module(self.server_name + '.service')
        except ImportError:
            logger.warning('{} has no service.py so init will be ignore.'.format(self.server_name))

    def remote_connect(self, remote_name, remote_host):
        for cnf in self.remote_list:
            _name = cnf.get('root_name')
            if remote_name == _name:
                port = cnf.get('root_port')
                if not remote_host:
                    addr = ('localhost', port)
                else:
                    addr = (remote_host, port)
                self.remote[remote_name].connect(addr)
                break

    async def main(self):
        server = await asyncio.start_server(
            handle_echo, '127.0.0.1', 8888)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

    def start(self):
        self.config()
        logger.info('{} started'.format(self.server_name))

        asyncio.run()


if __name__ == '__main__':
    pass
