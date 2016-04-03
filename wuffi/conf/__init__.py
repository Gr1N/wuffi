# -*- coding: utf-8 -*-

"""
Settings and configuration for `wuffi`.

Values will be read from the module specified by the `WUFFI_SETTINGS_MODULE` environment
variable, and then from `wuffi.conf.global_settings`; see the global settings file for
a list of all possible variables.

NOTE: The idea of settings organization got from `django` project.
"""

import importlib
import os

from wuffi.conf import global_settings
from wuffi.core.exceptions import ImproperlyConfigured
from wuffi.helpers.functional import EMPTY, LazyObject

__all__ = (
    'settings',
)


ENVIRONMENT_VARIABLE = 'WUFFI_SETTINGS_MODULE'


class LazySettings(LazyObject):
    """
    A lazy proxy for either global `wuffi` settings or a custom settings object.
    """
    def _setup(self, name=None):
        """
        Load the settings module pointed to by the environment variable. This
        is used the first time we need any settings at all, if the user has not
        previously configured the settings manually.
        """
        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            desc = ('setting %s' % name) if name else 'settings'
            raise ImproperlyConfigured(
                'Requested %s, but settings are not configured.'
                ' You must either define the environment variable %s.'
                % (desc, ENVIRONMENT_VARIABLE))

        self._wrapped = Settings(settings_module)

    def __repr__(self):
        # Hardcode the class name as otherwise it yields 'Settings'.
        if self._wrapped is EMPTY:
            return '<LazySettings [Unevaluated]>'
        return '<LazySettings "%(settings_module)s">' % {
            'settings_module': self._wrapped.SETTINGS_MODULE,
        }

    def __getattr__(self, name):
        if self._wrapped is EMPTY:
            self._setup(name)
        return getattr(self._wrapped, name)


class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    pass


class Settings(BaseSettings):
    def __init__(self, settings_module):
        # update this dict from global settings (but only for ALL_CAPS settings)
        for setting in dir(global_settings):
            if setting.isupper():
                setattr(self, setting, getattr(global_settings, setting))

        # store the settings module in case someone later cares
        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        tuple_settings = ()
        self._explicit_settings = set()
        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)

                if (setting in tuple_settings and
                        not isinstance(setting_value, (list, tuple))):
                    raise ImproperlyConfigured('The %s setting must be a list or a tuple.'
                                               ' Please fix your settings.' % setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

    def __repr__(self):
        return '<%(cls)s "%(settings_module)s">' % {
            'cls': self.__class__.__name__,
            'settings_module': self.SETTINGS_MODULE,
        }


settings = LazySettings()
