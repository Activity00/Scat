# coding: utf-8

"""
@author: 武明辉 
@time: 2018/2/10 19:37
"""

from scat.service import web_service, ws_service


@web_service
class EnterStd:
    URL = r'/tournament/enter-std/'

    def data_received(self, chunk):
        pass

    def get(self, *args, **kwargs):
        self.write('enter std success')


@ws_service
class Game:

    def check_origin(self, origin):
        return True

    def on_message(self, message):
        self.write_message(message)

#
# import tornado.websocket
#
# class A(tornado.websocket.WebSocketHandler):
#     def on_message(self, message):
#         self.write_message('xxx')


