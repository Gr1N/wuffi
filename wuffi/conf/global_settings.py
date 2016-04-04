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
