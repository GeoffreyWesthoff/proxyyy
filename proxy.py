from sanic import Sanic, response
from sanic.response import json

import aiohttp
import traceback

import asyncio

import uvloop


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

app = Sanic()


@app.listener('before_server_start')
async def init_http(app, loop):
    app.http = aiohttp.ClientSession(loop=loop)


@app.listener('before_server_stop')
async def close_http(app, loop):
    await app.http.close()


@app.route('/')
async def get_image(request):
    url = request.args.get('url', None)
    if url:
        try:
            async with app.http.get(url) as r:
                c = await r.content.read()
                return response.raw(c)
        except Exception as e:
            print(e, ''.join(traceback.format_tb(e.__traceback__)))
            return json({'status': 500, 'error': str(e)}), 500
    else:
        return json({"status": 400, "error": "No image URL provided"}), 400


if __name__ == '__main__':
    app.run()
