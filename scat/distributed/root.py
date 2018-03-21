# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 13:09
"""
from scat.distributed.child import ChildsManager, Child
from scat.rpc.handler import RPCHandler


class RPCRoot(RPCHandler):
    def __init__(self, service=None):
        self.service = service
        self.childs_manager = ChildsManager()

    def remote_regist(self, name, transport):
        child = Child(name, name, transport)
        self.childs_manager.add_child(child)
        self.on_child_connect(child)

    def remote_call_target(self, command, *args, **kwargs):
        self.service.call_target(command, *args, **kwargs)

    def on_child_connect(self, child):
        pass


class NETRoot:
    def __init__(self, service):
        self.service = service
        self.childs_manager = ChildsManager()

    def remote_regist(self, name, transport):
        child = Child(name, name, transport)
        self.childs_manager.add_child(child)
        self.on_child_connect(child)

    def remote_call_target(self, command, *args, **kwargs):
        self.service.call_target(command, *args, **kwargs)

    def on_child_connect(self, child):
        pass
