# -*- coding: utf-8 -*-

import os

import aiohttp_jinja2
import jinja2

from wuffi.conf import settings

__all__ = (
    'setup_templates',
)


def setup_templates(app):
    """
    Initializes jinja2 environment.
    """
    search_paths = [
        os.path.join(settings.BASE_DIR, path)
        for path in settings.TEMPLATES.get('DIRS', {})
    ]

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(search_paths))
