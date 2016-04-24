# -*- coding: utf-8 -*-

import os

import sqlalchemy as sa

from wuffi.conf import settings
from wuffi.core.db import DEFAULT_DATABASE_ALIAS

__all__ = (
    'target_url',
    'target_metadata',

    'run_offline',
    'run_online',
)


def target_url():
    target_settings = settings.DATABASES[DEFAULT_DATABASE_ALIAS]
    return sa.engine.url.URL(
        target_settings['BACKEND'].split('.')[-1],
        username=target_settings['USER'], password=target_settings['PASSWORD'],
        host=target_settings['HOST'], port=target_settings['PORT'],
        database=target_settings['DATABASE']
    )


def target_metadata():
    from wuffi.helpers.module_loading import import_module

    apps_dir = os.path.join(settings.BASE_DIR, 'apps')
    apps = [
        x for x in os.listdir(apps_dir)
        if os.path.isdir(os.path.join(apps_dir, x)) and x not in ('__pycache__',)
    ]

    modules = [
        import_module('apps.{app}.tables'.format(app=app))
        for app in apps
    ]

    metadatas = [
        x for x in sum(
            (list(module.__dict__.values()) for module in modules), []
        ) if isinstance(x, sa.MetaData)
    ]

    m = sa.MetaData()
    for metadata in metadatas:
        for t in metadata.tables.values():
            t.tometadata(m)

    return m


def run_offline(context):
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    :param context: Alembic context
    """
    context.configure(url=target_url(), target_metadata=target_metadata(),
                      literal_binds=True)

    with context.begin_transaction():
        context.run_migrations()


def run_online(context):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    :param context: Alembic context
    """
    connectable = sa.create_engine(target_url(), poolclass=sa.pool.NullPool)

    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata())

        with context.begin_transaction():
            context.run_migrations()
