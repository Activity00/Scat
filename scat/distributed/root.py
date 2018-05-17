from twisted.spread import pb
from scat.distributed.child import Child, ChildManager
from scat.utils.logutil import ScatLog

logger = ScatLog.get_logger()


class BilateralBroker(pb.Broker):
    def connectionLost(self, reason):
        client_id = self.transport.sessionno
        logger.warning("node [%d] losed" % client_id)
        self.factory.root.drop_child_session_id(client_id)
        pb.Broker.connectionLost(self, reason)


class BilateralFactory(pb.PBServerFactory):
    protocol = BilateralBroker


class PBRoot(pb.Root):

    def __init__(self, service=None):
        self.service = service
        self.child_manager = ChildManager()

    def add_service_channel(self, service):
        self.service = service

    def remote_register(self, name, transport):
        """
         远端结点注册
        :param name:
        :param transport:
        :return:
        """

        logger.info('node [%s] register ready' % name)
        child = Child(self.child_manager.generate_child_id(), name, transport)
        self.child_manager.add_child(child)
        self.do_child_connect(name, transport)

    def do_child_connect(self, name, transport):
        """当node节点连接时的处理
        """
        pass

    def remote_call_target(self, command, *args, **kwargs):
        data = self.service.call_target(command, *args, **kwargs)
        return data

    def drop_child(self, *args, **kwargs):
        """删除子节点记录"""
        self.child_manager.drop_child(*args, **kwargs)

    def drop_child_by_id(self, child_id):
        """删除子节点记录"""
        self.do_child_lost_connect(child_id)
        self.child_manager.drop_child_by_id(child_id)

    def do_child_lost_connect(self, child_id):
        """当node节点断开时的处理"""
        pass

    def drop_child_session_id(self, session_id):
        """删除子节点记录"""
        child = self.child_manager.get_child_by_session_id(session_id)
        if not child:
            logger.warning('not found session_id (%s) in method drop_child_session_id' % session_id)
            return
        child_id = child.id
        self.do_child_lost_connect(child_id)
        self.child_manager.drop_child_by_id(child_id)

    def call_child(self, key, *args, **kwargs):
        """
            @param childId: int
            return Defered Object
        """
        return self.child_manager.call_child(key, *args, **kwargs)

    def call_child_by_name(self, child_name, *args, **kw):
        return self.child_manager.call_child_by_name(child_name, *args, **kw)
