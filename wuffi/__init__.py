# -*- coding: utf-8 -*-

__all__ = (
    'get_application',
)


async def get_application(loop=None):
    from aiohttp import web

    from wuffi.conf import settings
    from wuffi.core.cache import DEFAULT_CACHE_ALIAS, get_caches
    from wuffi.core.db import DEFAULT_DATABASE_ALIAS, get_databases
    from wuffi.helpers.module_loading import import_string

    def get_router():
        return import_string('{}.router'.format(settings.ROOT_ROUTESCONF))

    def get_middlewares():
        return [import_string(func) for func in settings.MIDDLEWARE_FUNCTIONS]

    application = web.Application(loop=None,
                                  router=get_router(),
                                  middlewares=get_middlewares(),
                                  debug=settings.DEBUG)

    # Initialize databases
    dbs = await get_databases()
    if dbs:
        application['dbs'] = dbs
        application['db'] = dbs[DEFAULT_DATABASE_ALIAS]

        async def close_databases(application):
            for cache in application['dbs'].values():
                cache.close()

        application.on_shutdown.append(close_databases)

    # Initialize caches
    caches = await get_caches()
    if caches:
        application['caches'] = caches
        application['cache'] = caches[DEFAULT_CACHE_ALIAS]

        async def close_caches(application):
            for cache in application['caches'].values():
                cache.close()

        application.on_shutdown.append(close_caches)

    return application
