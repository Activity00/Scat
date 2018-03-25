import tornado.web
from twisted.spread import pb
from twisted.python import util
tornado.platform.twisted.install()
from twisted.internet import reactor

class MyHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        print('web')
        self.write('就这么刘')


factory = pb.PBClientFactory()
reactor.connectTCP("localhost", 8789, factory)

d = factory.getRootObject()

d.addCallback(lambda object: object.callRemote("echo", "hello network"))
d.addCallback(lambda echo: 'server echoed: '+echo)
d.addErrback(lambda reason: 'error: '+str(reason.value))
d.addCallback(util.println)
d.addCallback(lambda _: reactor.stop())


