# -*- coding: utf-8 -*-

import importlib

__all__ = (
    'import_string',
)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    module_path, attribute_name = dotted_path.rsplit('.', 1)
    module = importlib.import_module(module_path)

    return getattr(module, attribute_name)
