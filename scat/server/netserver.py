# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 13:58
"""
from tornado import iostream, gen
from tornado.http1connection import _QuietException
from tornado.log import gen_log
from tornado.tcpserver import TCPServer

from scat.server import NetConnection


class NetServer(TCPServer):
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self._connections = set()
        super(NetServer, self).__init__(*args, **kwargs)

    @gen.coroutine
    def handle_stream(self, stream, address):
        conn = NetConnection(stream)
        self._connections.add(conn)
        try:
            while True:
                try:
                    ret = yield conn.read_response(self.app)
                except (iostream.StreamClosedError,
                        iostream.UnsatisfiableReadError):
                    return
                except _QuietException:
                    # This exception was already logged.
                    conn.close()
                    return
                except Exception:
                    gen_log.error("Uncaught exception", exc_info=True)
                    conn.close()
                    return
                if not ret:
                    return
                yield gen.moment
        finally:
            conn.close()


if __name__ == '__main__':
    pass
