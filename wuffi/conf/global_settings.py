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
    'wuffi.middleware.clickjacking.middleware_factory',
)

MIDDLEWARE_HEADERS = {
    'X-Backend-Host': socket.gethostname(),
    'X-Backend-Pid': os.getpid(),
    'X-Backend-Start-At': datetime.utcnow().isoformat(),
}

MIDDLEWARE_CLICKJACKING_X_FRAME_OPTIONS = 'SAMEORIGIN'

####################
# DATABASE         #
####################

DATABASES = {
    # 'default': {
    #     'BACKEND': 'wuffi.core.db.backends.postgresql',
    #     'HOST': 'localhost',
    #     'PORT': 5432,
    #     'USER': None,
    #     'PASSWORD': None,
    #     'DATABASE': None,
    #     'POOLSIZE': 10,
    # },
    # 'default': {
    #     'BACKEND': 'wuffi.core.db.backends.mysql',
    #     'HOST': 'localhost',
    #     'PORT': 3306,
    #     'USER': None,
    #     'PASSWORD': None,
    #     'DATABASE': None,
    #     'POOLSIZE': 10,
    #     'AUTOCOMMIT': True,
    # },
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
    #     'DATABASE': 0,
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
