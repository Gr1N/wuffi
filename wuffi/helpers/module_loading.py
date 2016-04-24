# -*- coding: utf-8 -*-

import importlib

__all__ = (
    'import_string',
    'import_module',
)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    module_path, attribute_name = dotted_path.rsplit('.', 1)
    module = importlib.import_module(module_path)

    return getattr(module, attribute_name)


def import_module(dotted_path):
    """
    Import a dotted module path. Raise ImportError if the import failed.
    """
    return importlib.import_module(dotted_path)
