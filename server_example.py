import asyncio

import aiohttp
from aiohttp import web


async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def main():
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8889)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    return server


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


loop = asyncio.get_event_loop()
# add stuff to the loop
app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

# set up aiohttp - like run_app, but non-blocking
runner = aiohttp.web.AppRunner(app)
loop.run_until_complete(runner.setup())
site = aiohttp.web.TCPSite(runner, host='127.0.0.1', port=8888)
loop.run_until_complete(site.start())
loop.run_until_complete(main())
print('init done.')
loop.run_forever()
