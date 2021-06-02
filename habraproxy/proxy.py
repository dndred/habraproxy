from typing import Tuple, Any, Dict
from urllib.parse import urljoin

from aiohttp import web, ClientSession
from aiohttp.web_request import Request

from .config import Config
from .logging import get_module_logger
from .parser import Habraparser


class Habraproxy:
    _config = Config.get_instance()
    _log = get_module_logger(__name__)

    def __init__(self, loop) -> None:
        self._loop = loop
        self._app = web.Application()
        self._app.router.add_route('GET', '/{tail:.*}', self._handler)

    async def _handler(self, request: Request):
        self._log.info(request.path_qs)
        url = urljoin(self._config.remote_url, request.path_qs)
        session = ClientSession(loop=self._loop)
        response = await session.get(url)
        try:
            body = await response.content.read()
            headers = dict(response.headers)
            del headers['Content-Encoding']
            del headers['Transfer-Encoding']
            body, headers = self._response_middleware(body, headers)
        except Exception as e:
            self._log.exception(f'error={e} url={url}', exc_info=True)
            return web.HTTPInternalServerError()
        finally:
            await session.close()
        return web.Response(body=body, headers=headers)

    def _response_middleware(self, body: bytes, headers: Dict) -> Tuple[Any, Dict]:
        if headers['Content-Type'] == 'text/html; charset=UTF-8':
            parser = Habraparser(body)
            body = parser.process()
        return body, headers

    def start(self):
        self._log.info(f'Habraproxy start at {self._config.local_url}')
        web.run_app(
            self._app,
            host=self._config.bind_host,
            port=self._config.port,
            print=lambda _: ...,
        )
