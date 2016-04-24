# -*- coding: utf-8 -*-

from wuffi.conf import settings
from wuffi.core.exceptions import ImproperlyConfigured
from wuffi.helpers.module_loading import import_string

__all__ = (
    'DEFAULT_DATABASE_ALIAS',

    'get_databases',

    'generate_sql_create',
    'generate_sql_drop',
)


DEFAULT_DATABASE_ALIAS = 'default'


async def get_databases():
    """
    Initializes databases according to the settings.
    """
    if not settings.DATABASES:
        return {}

    if DEFAULT_DATABASE_ALIAS not in settings.DATABASES:
        raise ImproperlyConfigured('Default `{}` cache alias not defined in'
                                   ' `DATABASES` setting'.format(DEFAULT_DATABASE_ALIAS))

    dbs = {}
    for alias, options in settings.DATABASES.items():
        options = options.copy()
        options = {k.lower(): v for k, v in options.items()}

        backend = options.pop('backend')
        backend = import_string('{}.connect'.format(backend))

        dbs[alias] = await backend(**options)

    return dbs
