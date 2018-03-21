# coding: utf-8

"""
@author: 武明辉 
@time: 2018/1/27 12:40
"""
from tornado import iostream, gen
from tornado.concurrent import Future
from tornado.http1connection import _QuietException, _ExceptionLoggingContext
from tornado.log import gen_log, app_log


class RPCServerConnectionDelegate:
    def start_request(self, server_conn, request_conn):
        """This method is called by the server when a new request has started.

        :arg server_conn: is an opaque object representing the long-lived
               (e.g. tcp-level) connection.
        :arg request_conn: is a `.RPCConnection` object for a single
              request/response exchange.

             This method should return a `.RPCMessageDelegate`.
        """
        raise NotImplementedError

    def on_close(self, server_conn):
        pass


class RPCServerConnection:
    def __init__(self, stream):
        self.stream = stream
        self._serving_future = None

    def start_serving(self, delegate):
        assert isinstance(delegate, RPCServerConnectionDelegate)
        self._serving_future = self._server_request_loop(delegate)
        # Register the future on the IOLoop so its errors get logged.
        self.stream.io_loop.add_future(self._serving_future,
                                       lambda f: f.result())

    @gen.coroutine
    def _server_request_loop(self, delegate):
        try:
            conn = RPC2Connection(self.stream, False)
            request_delegate = delegate.start_request(self, conn)
            try:
                ret = yield conn.read_response(request_delegate)
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
            delegate.on_close(self)


class RPCConnection:
    # interface of RPC protocol
    def read_response(self, request_delegate):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError


class RPC2Connection(RPCConnection):
    # main implementation of RPC2.0
    def __init__(self, stream, is_client=False, timeout=None):
        self.stream = stream
        self.is_client = is_client
        self.timeout = timeout
        self._finish_future = Future()

    def read_response(self, delegate):
        """Read a single RPC response.
           Typical client-mode usage is to write a request using `write_headers`,
           `write`, and `finish`, and then call ``read_response``.
            :arg delegate: a `.RPCMessageDelegate`
            Returns a `.Future` that resolves to None after the full response has
            been read.
        """
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
