# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 10:04
"""
from scat.rpc.client import AsyncRPCClient


def callRemote(obj, func_name, *args, **kw):
    return obj.callRemote(func_name, *args, **kw)


class RemoteObject(object):
    """远程调用对象"""
    def __init__(self, name):
        self.name = name
        self.addr = None
        self.client = AsyncRPCClient()

    def connect(self, addr):
        """初始化远程调用对象"""
        self.addr = addr
        self.client.start(addr[0], addr[1])
        self.client.delegate.regist_node(self.name)

    def reconnect(self):
        """重新连接"""
        self.connect(self.addr)

    def addServiceChannel(self, service):
        """设置引用对象"""
        self.client.addService(service)


if __name__ == '__main__':
    pass
