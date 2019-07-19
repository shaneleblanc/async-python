from flask import Flask, escape, request, json, session
from uuid import uuid4  # for generating secret
import aiohttp
import asyncio

app = Flask(__name__)


async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.read()
            return {
                "resp": response,
                "html": html,
                "url": url,
            }


@app.route("/")
async def count():
    urls = []
    for x in range(1, 4):
        urls.append(f'https://postman-echo.com/get?count={x}')
    futures = [asyncio.ensure_future(fetch(url)) for url in urls]

    output = ""
    for future in futures:
        try:
            resp = await future
        except Exception as error:
            output += f"Failed: {error}"
            continue
        else:
            data = json.loads(resp['html'].decode())
            output += json.dumps(data['args'])
            output += '\n'

    return output

if __name__ == '__main__':
    app.secret_key = str(uuid4())
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run()
