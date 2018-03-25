import tornado.platform.twisted

from twisted.internet import protocol
from tornado.ioloop import IOLoop
from tornado.web import Application
from twisted.protocols.basic import LineReceiver
import tornado.web
from twisted.python import log
from tornado.log import *
tornado.platform.twisted.install()
from twisted.internet import reactor


class Echo(LineReceiver):
    def lineReceived(self, line):
        print(line)
        log.msg('xxxxxxxxx')
        app_log.warning('ewwwwwwwwwwwwwwwwwww')
        gen_log.warning('werewrew')
        gen_log.info('xfsrewrewadf')
        app_log.debug('ewwwwwwwwwwwwwwwwwww')
        self.sendLine(b'xxoo')


class MyHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        print('web')
        log.msg('fsadf')
        access_log.info('ekskskkskskskks')
        app_log.warning('ewwwwwwwwwwwwwwwwwww')
        gen_log.warning('werewrew')
        gen_log.info('xfsrewrewadf')
        self.write('就这么刘')

factory = protocol.ServerFactory()
factory.protocol = Echo

reactor.listenTCP(9000, factory)

application = Application(handlers=[(r'/', MyHandler, )])
application.listen(8000)

IOLoop.current().start()
