import asyncio
import importlib
from asyncio import StreamReader, StreamReaderProtocol

import aiohttp
from aiohttp import web


class ScatServer:
    """ it can be used for single server """

    def __init__(self, server_name):
        self.server_name = server_name

    def handle_echo(self, r, w):
        print('来啦老弟')
        w.close()

    async def handle(self, request):
        name = request.match_info.get('name', "Anonymous")
        text = "Hello, " + name
        return web.Response(text=text)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
                else:
                    await ws.send_str(msg.data + '/answer')
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                      ws.exception())

        print('websocket connection closed')
        return ws

    async def main(self, port):
        loop = asyncio.get_event_loop()

        def factory():
            reader = StreamReader()
            protocol = StreamReaderProtocol(reader, self.handle_echo, loop=loop)
            return protocol

        return await loop.create_server(factory, port=port)

    def config(self):
        loop = asyncio.get_event_loop()
        tcp_port = 8888
        http_port = 8889

        # TCP
        if tcp_port:
            server = loop.run_until_complete(self.main(tcp_port))
            addr = server.sockets[0].getsockname()
            print(f'TCP Serving on {addr!r}')

        # HTTP WEB
        if http_port:
            app = web.Application()
            runner = web.AppRunner(app)
            loop.run_until_complete(runner.setup())
            app.router._frozen = False
            site = web.TCPSite(runner, port=http_port)
            print(f'Serving on tcp started.')
            loop.run_until_complete(site.start())

            app.add_routes([web.get('/', self.handle),
                            web.get('/{name}', self.handle),
                            web.get('/ws', self.websocket_handler)])

        try:
            importlib.import_module(self.server_name)
        except ImportError:
            print(f'{self.server_name} has no service.py so init will be ignore.')

    def start(self):
        self.config()
        asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    ScatServer('game').start()
