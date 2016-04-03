# -*- coding: utf-8 -*-

__all__ = (
    'get_application',
)


async def get_application(loop=None):
    import importlib

    from aiohttp import web

    from wuffi.conf import settings

    def get_router():
        return importlib.import_module(settings.ROOT_ROUTESCONF).router

    def get_middlewares():
        return ()

    application = web.Application(loop=None,
                                  router=get_router(),
                                  middlewares=get_middlewares(),
                                  debug=settings.DEBUG)

    return application
