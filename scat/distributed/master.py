# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 14:31
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
import subprocess

from tornado import ioloop
from tornado.httpserver import HTTPServer
from tornado.log import *
from tornado.web import Application

from scat.distributed.root import PBRoot, BilateralFactory
from scat.server.globalobject import GlobalObject
from scat.service import Service
from scat.distributed import master_service


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

    def master_app(self):
        master_config = settings.MASTER

        root = PBRoot(Service("root_service"))
        reactor.listenTCP(master_config['root_port'], BilateralFactory(root))

        web_root = Application()  # web use a application contains handler
        http_server = HTTPServer(web_root)
        http_server.listen(master_config['web_port'])

        GlobalObject().root = root
        GlobalObject().web_root = web_root

        importlib.reload(master_service)
        GlobalObject().root.do_child_connect = self.do_child_connect
        GlobalObject().root.do_child_lost_connect = self.do_child_lost_connect

    def start(self, server_name, mode):
        if mode == MULTI_SERVER_MODE:
            self.master_app()
            server_config = settings.SERVERS
            for server_name in server_config.keys():
                cmds = 'python manage.py start_server %s' % server_name
                subprocess.Popen(cmds, shell=False)

            ioloop.IOLoop.current().start()
        elif mode == SINGLE_SERVER_MODE:
            cmds = 'python manage.py start_server %s' % server_name
            subprocess.Popen(cmds, shell=True)
        else:  # MASTER_SERVER_MODE
            self.master_app()
            ioloop.IOLoop.current().start()

    @staticmethod
    def do_child_connect(name, transport):
        """when server node connect to master excuted
        """

        server_config = GlobalObject().json_config.get('servers', {}).get(name, {})
        remoteport = server_config.get('remoteport', [])
        child_host = transport.broker.transport.client[0]
        root_list = [rootport.get('rootname') for rootport in remoteport]
        GlobalObject().remote_map[name] = {"host": child_host, "root_list": root_list}
        # 通知有需要连的node节点连接到此root节点
        for servername, remote_list in GlobalObject().remote_map.items():
            remote_host = remote_list.get("host", "")
            remote_name_host = remote_list.get("root_list", "")
            if name in remote_name_host:
                GlobalObject().root.callChild(servername, "remote_connect", name, remote_host)
        # 查看当前是否有可供连接的root节点
        master_node_list = GlobalObject().remote_map.keys()
        for root_name in root_list:
            if root_name in master_node_list:
                root_host = GlobalObject().remote_map[root_name]['host']
                GlobalObject().root.callChild(name, "remote_connect", root_name, root_host)

    @staticmethod
    def do_child_lost_connect(child_id):
        try:
            del GlobalObject().remote_map[child_id]
        except Exception as e:
            # log.msg(str(e))
            print(str(e))
