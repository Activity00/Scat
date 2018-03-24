from twisted.spread import pb
from twisted.internet import reactor

from scat.service import Service


def call_remote(obj, func_name, *args, **kwargs):
    return obj.callRemote(func_name, *args, **kwargs)


class ProxyReference(pb.Referenceable):
    def __init__(self):
        self._service = Service('proxy')

    def add_service(self, service):
        self._service = service

    def remote_call_child(self, command, *arg, **kw):
        return self._service.call_target(command, *arg, **kw)


class RemoteObject:
    """
    remote node include master and RMI root node
    """
    def __init__(self, name):
        self.name = name
        self._factory = pb.PBClientFactory()
        self._reference = ProxyReference()
        self._addr = None

    def connect(self, addr):
        self._addr = addr
        reactor.connectTCP(addr[0], addr[1], self._factory)
        self.register()

    def register(self):
        defered_remote = self._factory.getRootObject()
        defered_remote.addCallback(call_remote, 'register', self.name, self._reference)

    def reconnect(self):
        self.connect(self._addr)

    def add_service_channel(self, service):
        self._reference.addService(service)

    def call_remote(self, command_id, *args, **kw):
        defered_remote = self._factory.getRootObject()
        return defered_remote.addCallback(call_remote, 'call_target', command_id, *args, **kw)



