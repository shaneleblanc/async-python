import aiohttp
import asyncio
from quart import Quart, json, session
import time

app = Quart(__name__)


async def fetch(url, counter):
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
    start = time.time()
    urls = [[f'https://postman-echo.com/get?count={x}', x] for x in range(1, 101)]
    futures = [asyncio.ensure_future(fetch(url[0], url[1])) for url in urls]

    output = ""
    for future in futures:
        try:
            resp = await future
        except Exception as error:
            output += f'<br> Failed: {error}'
            continue
        else:
            data = json.loads(resp['html'].decode())
            now = time.time()
            output += f'<br> {resp["url"]} responded with  {json.dumps(data["args"])} ({now - start} seconds elapsed)'

    end = time.time()
    output += f'<p> This all took {(end - start)} seconds.</p>'
    return output

if __name__ == "__main__":
    app.config['SECRET_KEY'] = '1324912'
    app.run()
