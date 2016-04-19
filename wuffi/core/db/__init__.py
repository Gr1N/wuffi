# -*- coding: utf-8 -*-

import io

import sqlalchemy

from wuffi.conf import settings
from wuffi.core.exceptions import ImproperlyConfigured
from wuffi.helpers.module_loading import import_string

__all__ = (
    'DEFAULT_DATABASE_ALIAS',

    'get_databases',

    'generate_sql_create',
    'generate_sql_drop',
)


DEFAULT_DATABASE_ALIAS = 'default'


async def get_databases():
    """
    Initializes databases according to the settings.
    """
    if not settings.DATABASES:
        return {}

    if DEFAULT_DATABASE_ALIAS not in settings.DATABASES:
        raise ImproperlyConfigured('Default `{}` cache alias not defined in'
                                   ' `DATABASES` setting'.format(DEFAULT_DATABASE_ALIAS))

    dbs = {}
    for alias, options in settings.DATABASES.items():
        options = options.copy()
        options = {k.lower(): v for k, v in options.items()}

        backend = options.pop('backend')
        backend = import_string('{}.connect'.format(backend))

        dbs[alias] = await backend(**options)

    return dbs


def _get_database_mock(backend):
    buf = io.StringIO()

    def dump(sql, *args, **kwargs):
        buf.write(str(sql.compile(dialect=engine.dialect)))

    engine = sqlalchemy.create_engine('{}://'.format(backend), echo=True,
                                      strategy='mock', executor=dump)

    return buf, engine


def generate_sql_create(metadata, backend):
    buf, engine = _get_database_mock()
    metadata.create_all(engine)
    return buf.getvalue()


def generate_sql_drop(metadata, backend):
    buf, engine = _get_database_mock()
    metadata.drop_all(engine)
    return buf.getvalue()
