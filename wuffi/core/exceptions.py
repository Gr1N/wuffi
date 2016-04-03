# -*- coding: utf-8 -*-

__all__ = (
    'ImproperlyConfigured',
)


class ImproperlyConfigured(Exception):
    """
    `wuffi` is somehow improperly configured
    """
    pass
