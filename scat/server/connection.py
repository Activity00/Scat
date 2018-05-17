# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 13:14
"""
from tornado import gen, iostream
from tornado.concurrent import Future
from tornado.http1connection import _ExceptionLoggingContext
from tornado.log import app_log


class LineReceived:
    # interface of LineReceived protocol
    def read_response(self, request_delegate):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class NetConnection(LineReceived):
    # main implementation
    def __init__(self, stream, timeout=None):
        self.stream = stream
        self.timeout = timeout
        self._finish_future = Future()

    def read_response(self, delegate):
        return self._read_message(delegate)

    @gen.coroutine
    def _read_message(self, delegate):
        try:
            while True:
                message_future = self.stream.read_until(b"\r\n")
                if self.timeout is None:
                    message_data = yield message_future
                else:
                    try:
                        message_data = yield gen.with_timeout(
                            self.stream.io_loop.time() + self.timeout,
                            message_future,
                            io_loop=self.stream.io_loop,
                            quiet_exceptions=iostream.StreamClosedError)
                    except gen.TimeoutError:
                        self.close()
                        raise gen.Return(False)

                with _ExceptionLoggingContext(app_log):
                    data = delegate.data_received(message_data)
                    self.stream.write(data)
        finally:
            self._clear_callbacks()

    def close(self):
        if self.stream is not None:
            self.stream.close()
        self._clear_callbacks()
        if not self._finish_future.done():
            self._finish_future.set_result(None)

    def _clear_callbacks(self):
        """Clears the callback attributes.

        This allows the request handler to be garbage collected more
        quickly in CPython by breaking up reference cycles.
        """
        self._write_callback = None
        self._write_future = None
        self._close_callback = None
        if self.stream is not None:
            self.stream.set_close_callback(None)


if __name__ == '__main__':
    pass
