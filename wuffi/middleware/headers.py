# -*- coding: utf-8 -*-

from aiohttp.web_exceptions import HTTPException

from wuffi.conf import settings

__all__ = (
    'middleware_factory',
)


async def middleware_factory(app, next_handler):
    async def middleware(request):
        try:
            response = await next_handler(request)
        except HTTPException as exc:
            response = exc

        if not response.started:
            for header, value in settings.MIDDLEWARE_HEADERS.items():
                response.headers[header] = str(value)

        return response
    return middleware
