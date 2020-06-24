"""
@author: 武明辉 
@time: 2018/1/20 14:31
"""

import importlib
import os
import subprocess

import asyncio

from scat.conf import settings
from scat.distributed.root import PBRoot, BilateralFactory
from scat import ScatObject
from scat.service import Service
from scat.distributed import master_service
from scat.utils.logutil import ScatLog

logger = ScatLog.get_logger()

MULTI_SERVER_MODE = 1
SINGLE_SERVER_MODE = 2
MASTER_SERVER_MODE = 3


class Master:
    def master_app(self):
        logger.info('Master starting...')
        master_config = settings.MASTER

        root = PBRoot(Service("root_service"))
        reactor.listenTCP(master_config['root_port'], BilateralFactory(root))

        web_root = web.Application()  # web use a application contains handler
        ScatObject.root = root
        ScatObject.web_root = web_root

        importlib.reload(master_service)
        ScatObject.root.do_child_connect = self.do_child_connect
        ScatObject.root.do_child_lost_connect = self.do_child_lost_connect

        logger.info('Master web listened {}'.format(master_config['web_port']))
        logger.info('Master root listened {}'.format(master_config['root_port']))

    def start(self, server_name, mode):
        if mode == MULTI_SERVER_MODE:
            self.master_app()
            server_config = settings.SERVERS
            for server_name in server_config.keys():
                cmds = 'python manage.py start_server %s' % server_name
                subprocess.Popen(cmds, shell=False)

            master_config = settings.MASTER
            web.run_app(ScatObject.web_root, port=master_config['web_port'])
        elif mode == SINGLE_SERVER_MODE:
            cmds = 'python manage.py start_server %s' % server_name
            subprocess.Popen(cmds, shell=True)
        else:  # MASTER_SERVER_MODE
            self.master_app()
            ioloop.IOLoop.current().start()

    @staticmethod
    def do_child_connect(name, transport):
        """
        when server node connect to master deal
        :param name: server name
        :param transport: server transport
        :return:
        """
        # 1. connect to master and add to Master->remote_map({"name": {"host":"127.0.0.1"}, [root_list]})
        server_config = settings.SERVERS.get(name, {})

        remote_list = server_config.get('remote_list', [])
        root_list = [root.get('root_name') for root in remote_list]

        child_host = transport.broker.transport.client[0]  # get server host str
        ScatObject.remote_map[name] = {'host': child_host, 'root_list': root_list}

        # 2. notify node that want to connect to this node.
        for server_name, remote_list in ScatObject.remote_map.items():
            """
            server_name: have connected to Master
            """
            remote_host = remote_list.get('host', '')
            remote_name_host = remote_list.get('root_list', '')
            if name in remote_name_host:
                ScatObject.root.call_child_by_name(server_name, 'remote_connect', name, remote_host)

        #  check if there is a root node to be connected.
        master_node_list = ScatObject.remote_map.keys()
        for root_name in root_list:
            if root_name in master_node_list:
                root_host = ScatObject.remote_map[root_name]['host']
                ScatObject.root.call_child_by_name(name, "remote_connect", root_name, root_host)

    @staticmethod
    def do_child_lost_connect(child_id):
        try:
            del ScatObject.remote_map[child_id]
        except Exception as e:
            logger.error(str(e))
