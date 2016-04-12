# -*- coding: utf-8 -*-

from aiohttp import web
from sqlalchemy import sql as sasql

from wuffi.core.db import DEFAULT_DATABASE_ALIAS

__all__ = (
    'ListMixin',
    'RetrieveMixin',

    'ListView',
    'RetrieveView',
)


class ListMixin(object):
    db_alias = DEFAULT_DATABASE_ALIAS

    select = None
    where = None
    order_by = None

    limit_kwarg = 'limit'
    limit_default = 50
    offset_kwarg = 'offset'
    offset_default = 0

    def db_connection(self):
        return self.request.app['dbs'][self.db_alias].acquire()

    def get_total(self):
        # TODO: return total count
        return -1

    async def get_list(self):
        query = self.get_query()
        query = self.paginate_query(query)

        async with self.db_connection() as conn:
            objs = await (await conn.execute(query)).fetchall()

        return [dict(obj) for obj in objs]

    def get_query(self):
        query = sasql.select(self.get_select())

        where = self.get_where()
        if where is not None:
            query = query.where(where)

        order_by = self.get_order_by()
        if order_by is not None:
            query = query.order_by(order_by)

        return query

    def get_select(self):
        return self.select

    def get_where(self):
        return self.where

    def get_order_by(self):
        return self.order_by

    def get_pagination(self):
        try:
            limit = int(self.request.GET.get(self.limit_kwarg))
        except Exception:
            limit = self.limit_default

        try:
            offset = int(self.request.GET.get(self.offset_kwarg))
        except Exception:
            offset = self.offset_default

        return limit, offset

    def paginate_query(self, query):
        limit, offset = self.get_pagination()
        return query.limit(limit).offset(offset)

    async def list(self):
        return web.json_response(data={
            'list': await self.get_list(),
            'total': self.get_total(),
        })


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

    async def details(self):
        obj = await self.get_object()

        return web.json_response(data=obj)


class ListView(ListMixin,
               web.View):
    async def get(self):
        return await self.list()


class RetrieveView(RetrieveMixin,
                   web.View):
    async def get(self):
        return await self.details()
