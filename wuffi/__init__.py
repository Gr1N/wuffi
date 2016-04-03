# -*- coding: utf-8 -*-

__all__ = (
    'get_application',
)


async def get_application(loop=None):
    from aiohttp import web

    from wuffi.conf import settings
    from wuffi.helpers.module_loading import import_string

    def get_router():
        return import_string('{}.router'.format(settings.ROOT_ROUTESCONF))

    def get_middlewares():
        return [import_string(func) for func in settings.MIDDLEWARE_FUNCTIONS]

    application = web.Application(loop=None,
                                  router=get_router(),
                                  middlewares=get_middlewares(),
                                  debug=settings.DEBUG)

    return application
