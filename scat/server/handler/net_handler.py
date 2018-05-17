# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/4 18:40
"""
import json

from tornado.websocket import WebSocketHandler


class NetHandlerBase:
    def __init__(self):
        pass

    def data_received(self, data):
        try:
            request_data = json.loads(data.decode())
        except Exception:
            return b'{"status": 400, "message": "not a json format"}\r\n'

        command = request_data.get('command')
        params = request_data.pop(command)
        if not command:
            return b'{"status": 400, "message": "params error"}\r\n'

        return self.dispatch(command, params)

    def dispatch(self, command, params):
        method = getattr(self, command, None)
        if not method:
            return b'{"status": 400, "message": "params error command not found"}\r\n'

        return method(params)


class NetHandler(NetHandlerBase):
    pass


class WebSocketNetHandler(WebSocketHandler):
    # TODO websocket support
    def data_received(self, chunk):
        pass

    def on_message(self, message):
        pass