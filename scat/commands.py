# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 19:14
"""
import fire
from tornado import ioloop

from scat.master import MASTER_SERVER_MODE, SINGLE_SERVER_MODE, MULTI_SERVER_MODE
from scat.server import ScatServer


class Commands:
    def createproject(self, name, path='.'):
        return 'create project {} path: {}'.format(name, path)

    def runserver(self, server_name='', mode=''):
        from scat.master import Master
        if mode == "single":
            if server_name == "master":
                mode = MASTER_SERVER_MODE
            else:
                mode = SINGLE_SERVER_MODE
        else:
            mode = MULTI_SERVER_MODE
            server_name = ''
        master = Master()
        master.start(server_name, mode)

    def start_server(self, server_name):
        server = ScatServer(server_name)
        server.start()

    def __str__(self):
        return 'Python manage.py COMMANDNAME --paras'


def execute_from_command_line():
    fire.Fire(Commands)
