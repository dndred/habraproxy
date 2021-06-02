import asyncio

from .proxy import Habraproxy

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    proxy = Habraproxy(loop)
    proxy.start()
