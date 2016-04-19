# -*- coding: utf-8 -*-

from http import HTTPStatus

from aiohttp import web
from sqlalchemy import sql as sasql

from wuffi.core.db import DEFAULT_DATABASE_ALIAS
from wuffi.views.generic.validation import ValidationMixin

__all__ = (
    'RelationalMixin',
    'RelationalObjectMixin',

    'CreateMixin',
    'ListMixin',
    'RetrieveMixin',
    'UpdateMixin',
    'DestroyMixin',

    'CreateView',
    'ListView',
    'RetrieveView',
    'UpdateView',
    'DestroyView',
    'ListCreateView',
    'RetrieveUpdateView',
    'RetrieveDestroyView',
    'RetrieveUpdateDestroyView',
)


class RelationalMixin(object):
    """
    Base class for all other relational views.
    """

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


class RelationalObjectMixin(RelationalMixin):
    """
    Base class for all other relational views that manipulate objects.
    """

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


class CreateMixin(object):
    """
    Create object.
    """

    async def create(self):
        v = self.get_validator()
        d = await self.get_document()

        if not v.validate(d):
            return web.json_response(data=v.errors, status=HTTPStatus.BAD_REQUEST)

        obj = await self.perform_create(v.document)

        return web.json_response(data=dict(obj), status=HTTPStatus.CREATED,
                                 headers=self.get_created_headers(obj))

    async def perform_create(self, document):
        query = self.table.insert().values(
            **document
        ).returning(*(self.table.c._all_columns))

        async with self.db_connection() as conn:
            result = await conn.execute(query)
            obj = await result.fetchone()

        return obj

    def get_created_headers(self, obj):
        return {}


class ListMixin(object):
    """
    List a queryset.
    """

    limit_url_kwarg = 'limit'
    limit_default = 50
    offset_url_kwarg = 'offset'
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
            limit = int(self.request.GET.get(self.limit_url_kwarg))
        except Exception:
            limit = self.limit_default

        try:
            offset = int(self.request.GET.get(self.offset_url_kwarg))
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


class RetrieveMixin(object):
    """
    Retrieve object.
    """

    async def details(self):
        obj = dict(await self.get_object())

        return web.json_response(data=obj)


class UpdateMixin(object):
    """
    Update object.
    """

    async def update(self):
        # Try to find object with specified primary key,
        # if object not found, then 404 exception raises
        await self.get_object()

        v = self.get_validator()
        d = await self.get_document()

        if not v.validate(d):
            return web.json_response(data=v.errors, status=HTTPStatus.BAD_REQUEST)

        obj = await self.perform_update(v.document)

        return web.json_response(data=dict(obj))

    async def perform_update(self, document):
        query = self.table.update()

        where = self.get_where()
        if where is not None:
            query = query.where(where)

        query = query.values(
            **document
        ).returning(*(self.table.c._all_columns))

        async with self.db_connection() as conn:
            result = await conn.execute(query)
            obj = await result.fetchone()

        return obj


class DestroyMixin(object):
    """
    Destroy object.
    """

    async def destroy(self):
        # Try to find object with specified primary key,
        # if object not found, then 404 exception raises
        await self.get_object()
        await self.perform_destroy()

        return web.json_response(status=HTTPStatus.NO_CONTENT)

    async def perform_destroy(self):
        query = self.table.delete()

        where = self.get_where()
        if where is not None:
            query = query.where(where)

        async with self.db_connection() as conn:
            await conn.execute(query)


class CreateView(RelationalMixin,
                 ValidationMixin,
                 CreateMixin,
                 web.View):
    """
    Concrete view for creating objects.
    """

    async def post(self):
        return await self.create()


class ListView(RelationalMixin,
               ListMixin,
               web.View):
    """
    Concrete view for listing a queryset.
    """

    async def get(self):
        return await self.list()


class RetrieveView(RelationalObjectMixin,
                   RetrieveMixin,
                   web.View):
    """
    Concrete view for retrieving objects.
    """

    async def get(self):
        return await self.details()


class UpdateView(RelationalObjectMixin,
                 ValidationMixin,
                 UpdateMixin,
                 web.View):
    """
    Concrete view for updating objects.
    """

    async def put(self):
        return await self.update()


class DestroyView(RelationalObjectMixin,
                  DestroyMixin,
                  web.View):
    """
    Concrete view for deleting objects.
    """

    async def delete(self):
        return await self.destroy()


class ListCreateView(RelationalMixin,
                     ValidationMixin,
                     ListMixin,
                     CreateMixin,
                     web.View):
    """
    Concrete view for listing a queryset or creating objects.
    """

    async def get(self):
        return await self.list()

    async def post(self):
        return await self.create()


class RetrieveUpdateView(RelationalObjectMixin,
                         ValidationMixin,
                         RetrieveMixin,
                         UpdateMixin,
                         web.View):
    """
    Concrete view for retrieving or updating objects.
    """

    async def get(self):
        return await self.details()

    async def put(self):
        return await self.update()


class RetrieveDestroyView(RelationalObjectMixin,
                          RetrieveMixin,
                          DestroyMixin,
                          web.View):
    """
    Concrete view for retrieving or deleting objects.
    """

    async def get(self):
        return await self.details()

    async def delete(self):
        return await self.destroy()


class RetrieveUpdateDestroyView(RelationalObjectMixin,
                                ValidationMixin,
                                RetrieveMixin,
                                UpdateMixin,
                                DestroyMixin,
                                web.View):
    """
    Concrete view for retrieving, updating or deleting objects.
    """

    async def get(self):
        return await self.details()

    async def put(self):
        return await self.update()

    async def delete(self):
        return await self.destroy()
