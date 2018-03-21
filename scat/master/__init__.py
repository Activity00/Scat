# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 14:31
"""
import importlib
import logging
import os
import subprocess

from tornado import ioloop
from tornado.web import Application
from tornado.httpserver import HTTPServer

from scat.master import webapp
from scat.rpc.server import RPCServer
from scat.server.globalobject import GlobalObject
from scat.server.handler.root_handler import RootHandler

logger = logging.getLogger(__name__)
MULTI_SERVER_MODE = 1
SINGLE_SERVER_MODE = 2
MASTER_SERVER_MODE = 3


setting_str = os.environ.get('SCAT_SETTINGS_MODULE', None)
if not setting_str:
    raise Exception
settings = importlib.import_module(setting_str)


class Master:
    def __init__(self):
        pass

    def masterapp(self):
        master_config = settings.MASTER

        root = RootHandler()    # deal the rpc method
        server = RPCServer(root)
        server.listen(master_config['root_port'])

        web_root = Application()  # web use a application contains handler
        http_server = HTTPServer(web_root)
        http_server.listen(master_config['web_port'])

        GlobalObject().root = root
        GlobalObject().web_root = web_root

        webapp.init_handlers()
    
    def start(self, server_name, mode):
        if mode == MULTI_SERVER_MODE:
            self.masterapp()
            server_config = settings.SERVERS
            for sername in server_config.keys():
                cmds = 'python manage.py start_server %s' % sername
                subprocess.Popen(cmds, shell=False)

            ioloop.IOLoop.current().start()
        elif mode == SINGLE_SERVER_MODE:
            cmds = 'python manage.py start_server %s' % server_name
            subprocess.Popen(cmds, shell=True)
        else:  # MASTER_SERVER_MODE
            self.masterapp()
            ioloop.IOLoop.current().start()


if __name__ == '__main__':
    pass
