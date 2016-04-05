# -*- coding: utf-8 -*-
"""
Default `wuffi` settings. Override these with settings in the module pointed to
by the `WUFFI_SETTINGS_MODULE` environment variable.
"""

####################
# CORE             #
####################

DEBUG = True

ROOT_ROUTESCONF = 'config.routes'

MIDDLEWARE_FUNCTIONS = (
    'wuffi.middleware.stats.middleware_factory',
)

####################
# CACHE            #
####################

CACHES = {
    # 'default': {
    #     'BACKEND': 'wuffi.core.cache.backends.redis',
    #     'HOST': 'localhost',
    #     'PORT': 6379,
    #     'PASSWORD': None,
    #     'DB': 0,
    #     'POOLSIZE': 1,
    #     'AUTO_RECONNECT': True,
    # },
    # 'default': {
    #     'BACKEND': 'wuffi.core.cache.backends.memcached',
    #     'HOST': 'localhost',
    #     'PORT': 11211,
    #     'POOLSIZE': 1,
    # },
}
