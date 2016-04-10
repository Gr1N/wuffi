# -*- coding: utf-8 -*-

from aiohttp import web
from sqlalchemy import sql as sasql

from wuffi.core.db import DEFAULT_DATABASE_ALIAS

__all__ = (
    'RetrieveMixin',
    'RetrieveView',
)


class RetrieveMixin(object):
    db_alias = DEFAULT_DATABASE_ALIAS

    select = None
    where = None

    async def get_object(self):
        query = self.get_query()

        async with self.request.app['dbs'][self.db_alias].acquire() as conn:
            obj = await (await conn.execute(query)).fetchone()

        if not obj:
            raise web.HTTPNotFound()

        return dict(obj)

    def get_query(self):
        query = sasql.select(self.get_select())

        where = self.get_where()
        if where is not None:
            query = query.where(where)

        return query

    def get_select(self):
        return self.select

    def get_where(self):
        return self.where


class RetrieveView(RetrieveMixin,
                   web.View):
    async def get(self):
        obj = await self.get_object()
        return web.json_response(data=obj)
