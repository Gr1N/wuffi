# -*- coding: utf-8 -*-

from wuffi.conf import settings
from wuffi.core.exceptions import ImproperlyConfigured
from wuffi.helpers.module_loading import import_string

__all__ = (
    'DEFAULT_CACHE_ALIAS',

    'get_caches',
)


DEFAULT_CACHE_ALIAS = 'default'


async def get_caches():
    """
    Initializes caches according to the settings.
    """
    if not settings.CACHES:
        return {}

    if DEFAULT_CACHE_ALIAS not in settings.CACHES:
        raise ImproperlyConfigured('Default `{}` cache alias not defined in'
                                   ' `CACHES` setting'.format(DEFAULT_CACHE_ALIAS))

    caches = {}
    for alias, options in settings.CACHES.items():
        options = options.copy()
        options = {k.lower(): v for k, v in options.items()}

        backend = options.pop('backend')
        backend = import_string('{}.connect'.format(backend))

        caches[alias] = await backend(**options)

    return caches
