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

        if response.started:
            return response

        # Don't set it if it's already in the response
        if response.headers.get('X-Frame-Options') is not None:
            return response

        # Don't set it if they added `x_frame_options_exempt` to response
        if getattr(response, 'x_frame_options_exempt', False):
            return response

        x_frame_options = settings.MIDDLEWARE_CLICKJACKING_X_FRAME_OPTIONS
        response.headers['X-Frame-Options'] = x_frame_options

        return response
    return middleware
