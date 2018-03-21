# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/20 14:27
"""
from tornado import gen, iostream
from tornado.http1connection import _QuietException
from tornado.log import gen_log
from tornado.tcpclient import TCPClient

from scat.rpc.connection import RPC2Connection


class AsyncRPCClient:
    def __init__(self, delegate=None):
        self.conn = None
        self.delegate = delegate

    def add_service(self, service):
        self.delegate = service

    @gen.coroutine
    def start(self, host, port):
        stream = yield TCPClient().connect(host, port)
        try:
            self.conn = RPC2Connection(stream, True)
            try:
                ret = yield self.conn.read_response(self.delegate)
            except (iostream.StreamClosedError,
                    iostream.UnsatisfiableReadError):
                return
            except _QuietException:
                # This exception was already logged.
                self.conn.close()
                return
            except Exception:
                gen_log.error("Uncaught exception", exc_info=True)
                self.conn.close()
                return
            if not ret:
                return
            yield gen.moment
        finally:
            self.conn.close()


