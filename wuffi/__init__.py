# -*- coding: utf-8 -*-

__all__ = (
    'get_application',
)


async def get_application(loop=None):
    from aiohttp import web

    from wuffi.conf import settings
    from wuffi.core.cache import DEFAULT_CACHE_ALIAS, get_caches
    from wuffi.core.db import DEFAULT_DATABASE_ALIAS, get_databases
    from wuffi.helpers.log import configure_logging
    from wuffi.helpers.module_loading import import_string
    from wuffi.template import configure_templates

    def get_router():
        return import_string('{}.router'.format(settings.ROOT_ROUTESCONF))

    def get_middlewares():
        return [import_string(func) for func in settings.MIDDLEWARE_FUNCTIONS]

    app = web.Application(loop=None,
                          router=get_router(),
                          middlewares=get_middlewares(),
                          debug=settings.DEBUG)

    # Initialize logging
    configure_logging(settings.LOGGING_CONFIG, settings.LOGGING)
    # Initialize template engine
    configure_templates(app)

    # Initialize databases
    dbs = await get_databases()
    if dbs:
        app['dbs'] = dbs
        app['db'] = dbs[DEFAULT_DATABASE_ALIAS]

        async def close_databases(app):
            for db in app['dbs'].values():
                db.close()
                await db.wait_closed()

        app.on_shutdown.append(close_databases)

    # Initialize caches
    caches = await get_caches()
    if caches:
        app['caches'] = caches
        app['cache'] = caches[DEFAULT_CACHE_ALIAS]

        async def close_caches(app):
            for cache in app['caches'].values():
                cache.close()

        app.on_shutdown.append(close_caches)

    return app
