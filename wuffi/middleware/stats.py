# -*- coding: utf-8 -*-

from datetime import datetime

__all__ = (
    'middleware_factory',
)


STARTED_AT = datetime.utcnow().isoformat()


async def middleware_factory(app, next_handler):
    async def middleware(request):
        try:
            response = await next_handler(request)
        except HTTPException as exc:
            response = exc

        if not response.started:
            response.headers['X-Server-Started-At'] = STARTED_AT

        return response
    return middleware
