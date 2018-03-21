from tornado.tcpserver import TCPServer
from scat.rpc.connection import RPCServerConnection, RPCServerConnectionDelegate


class RPCServer(TCPServer, RPCServerConnectionDelegate):
    def __init__(self, request_callback, *args, **kwargs):
        self._connections = set()
        self.request_callback = request_callback
        super(RPCServer, self).__init__(*args, **kwargs)

    def handle_stream(self, stream, address):
        """will be called when the new connection connected"""
        conn = RPCServerConnection(stream)
        self._connections.add(conn)
        conn.start_serving(self)

    def start_request(self, server_conn, request_conn):
        # return self.request_callback.start_request(server_conn, request_conn)
        return self.request_callback

    def on_close(self, server_conn):
        self._connections.remove(server_conn)


