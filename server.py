
import logging
from aiohttp import web
import asyncio
import aiohttp
import traceback





####################################################################################################



WEB_URL = "https://vegeta-private.onrender.com/"
WEB_SLEEP = 4*60



####################################################################################################






logger = logging.getLogger(__name__)
routes = web.RouteTableDef()



@routes.get('/', allow_head=True)

async def hello(request):

    return web.Response(text="Hello, world!")





def web_server():

    web_app = web.Application(client_max_size=300000)

    web_app.add_routes(routes)

    return web_app





async def keep_alive():

    if WEB_URL:

        while True:

            await asyncio.sleep(WEB_SLEEP)

            try:

                async with aiohttp.ClientSession(

                    timeout=aiohttp.ClientTimeout(total=10)

                ) as session:

                    async with session.get(WEB_URL) as resp:

                        logger.info(

                            "Pinged {} with response: {}".format(

                                WEB_URL, resp.status

                            )

                        )

            except asyncio.TimeoutError:

                logger.warning("Couldn't connect to the site URL..!")

            except Exception:

                traceback.print_exc()

