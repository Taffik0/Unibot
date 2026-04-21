import ssl
import certifi
import aiohttp

import asyncio
from aiovk.longpoll import BotsLongPoll
from aiovk import TokenSession, API
from aiovk.drivers import HttpDriver


async def main():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    a_session = aiohttp.ClientSession(connector=connector)
    session = TokenSession(access_token="vk1.a.cnjV02Ngwgvtg9s_EfTftOLCN8Rgly8THpEKmcmQ_kTUYR7Lxz7FhxYl29ZYOtRelII9jAKYHN0ZDNHDz9C1R7gq8706ptlL5hBWG2SBXnEHyi1oGPt2PE6E15WsbKXHnQVGMY-IC7GzT3pNUG0XK0XrvTNYNC568Pd3j3Ir3FkbrMhXhknF3OzPxiIg9pEpVYzocxv0ojib_6KKbC29MA",
                           driver=HttpDriver(session=a_session))
    api = API(session)
    longpoll = BotsLongPoll(api, group_id=237910774)
    print("start")
    async for event in longpoll.iter():
        print(event)
        if event["type"] == "message_new":
            print(event["object"]["message"]["text"])

if __name__ == "__main__":
    asyncio.run(main())
