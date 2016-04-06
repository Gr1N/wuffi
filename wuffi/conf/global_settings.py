# -*- coding: utf-8 -*-
"""
Default `wuffi` settings. Override these with settings in the module pointed to
by the `WUFFI_SETTINGS_MODULE` environment variable.
"""

import os
import socket
from datetime import datetime

####################
# CORE             #
####################

DEBUG = True

ROOT_ROUTESCONF = 'config.routes'

####################
# MIDDLEWARE       #
####################

MIDDLEWARE_FUNCTIONS = (
    'wuffi.middleware.headers.middleware_factory',
)

MIDDLEWARE_HEADERS = {
    'X-Backend-Host': socket.gethostname(),
    'X-Backend-Pid': os.getpid(),
    'X-Backend-Start-At': datetime.utcnow().isoformat(),
}

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
