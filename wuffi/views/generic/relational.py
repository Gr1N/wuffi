# -*- coding: utf-8 -*-

from aiohttp import web
from sqlalchemy import sql as sasql

from wuffi.core.db import DEFAULT_DATABASE_ALIAS

__all__ = (
    'RelationalMixin',

    'ListMixin',
    'RetrieveMixin',

    'ListView',
    'RetrieveView',
)


class RelationalMixin(object):
    db_alias = DEFAULT_DATABASE_ALIAS

    table = None

    select = None
    where = None
    order_by = None

    def db_connection(self):
        return self.request.app['dbs'][self.db_alias].acquire()

    def get_query(self):
        select = self.get_select()
        if not isinstance(select, (tuple, list,)):
            select = (select,)

        query = sasql.select(select)

        where = self.get_where()
        if where is not None:
            query = query.where(where)

        order_by = self.get_order_by()
        if order_by is not None:
            query = query.order_by(order_by)

        return query

    def get_select(self):
        return self.select or self.table

    def get_where(self):
        return self.where

    def get_order_by(self):
        return self.order_by


class ListMixin(RelationalMixin):
    limit_kwarg = 'limit'
    limit_default = 50
    offset_kwarg = 'offset'
    offset_default = 0

    async def get_total(self):
        query = self.table.count()

        where = self.get_where()
        if where is not None:
            query = query.where(where)

        async with self.db_connection() as conn:
            result = await conn.execute(query)
            total = await result.fetchone()

        return total[0]

    async def get_list(self):
        query = self.get_query()
        query = self.paginate_query(query)

        async with self.db_connection() as conn:
            result = await conn.execute(query)
            objs = await result.fetchall()

        return objs

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
        total = await self.get_total()
        if not total:
            return web.json_response(data={
                'list': [],
                'total': 0,
            })

        return web.json_response(data={
            'list': [dict(obj) for obj in await self.get_list()],
            'total': total,
        })


class RetrieveMixin(RelationalMixin):
    lookup_field = 'id'
    lookup_url_kwarg = None

    async def get_object(self):
        query = self.get_query()

        async with self.db_connection() as conn:
            result = await conn.execute(query)
            obj = await result.fetchone()

        if not obj:
            raise web.HTTPNotFound()

        return obj

    def get_where(self):
        assert self.lookup_field in self.table.c, (
            'Expected view {} should be used with table which has lookup'
            ' field named "{}". Fix your table, or set the `.lookup_field`'
            ' attribute on the view correctly'.format(
                self.__class__.__name__, self.lookup_field))

        url_kwargs = self.request.match_info
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in url_kwargs, (
            'Expected view {} to be called with a URL keyword argument'
            ' named "{}". Fix your URL conf, or set the `.lookup_field`'
            ' attribute on the view correctly'.format(
                self.__class__.__name__, lookup_url_kwarg))

        return getattr(self.table.c, self.lookup_field) == url_kwargs[lookup_url_kwarg]

    async def details(self):
        obj = dict(await self.get_object())

        return web.json_response(data=obj)


class ListView(ListMixin,
               web.View):
    async def get(self):
        return await self.list()


class RetrieveView(RetrieveMixin,
                   web.View):
    async def get(self):
        return await self.details()
