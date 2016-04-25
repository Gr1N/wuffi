# -*- coding: utf-8 -*-

import functools
import sys

import raven
import raven_aiohttp
from aiohttp.web_exceptions import HTTPException

from wuffi.conf import settings

__all__ = (
    'middleware_factory',
)


@functools.lru_cache(maxsize=None)
def get_client():
    return raven.Client(transport=raven_aiohttp.AioHttpTransport, context={
        'sys.argv': sys.argv[:],
    }, **settings.MIDDLEWARE_SENTRY)


async def middleware_factory(app, next_handler):
    async def middleware(request):
        try:
            return await next_handler(request)
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            client = get_client()

            if client.is_enabled():
                client.captureException(sys.exc_info(), data={
                    'request': {
                        'url': '{scheme}://{host}{path}'.format(
                            scheme=request.scheme,
                            host=request.host,
                            path=request.path
                        ),
                        'query_string': request.query_string,
                        'method': request.method,
                        'headers': {
                            k.title(): str(v)
                            for k, v in request.headers.items()
                        },
                        'data': await request.read(),
                    },
                })

            raise exc

    return middleware
