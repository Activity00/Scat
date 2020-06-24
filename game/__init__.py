from aiohttp import web


class Player(web.View):
    async def get(self):
        print(f'xxx{self}')
