# -*- coding: utf-8 -*-

import re

from aiohttp import web_urldispatcher

from wuffi.helpers.module_loading import import_string

__all__ = (
    'UrlDispatcher',
)


class UrlDispatcher(web_urldispatcher.UrlDispatcher):
    """
    Router with an :meth:`include_routes` method for including routes from
    separated. Includes all the methods `aiohttp.web.UrlDispatcher`
    with the addition of `add_resource`.

    Example:

    .. code-block:: python

        from aiohttp import web

        from wuffi.core.urls import UrlDispatcher


        async def index(request):
            return web.Response(body=b'Wuff Wuff')


        router = UrlDispatcher()
        router.add_route('GET', '/', index)
        router.include_routes('/todo', 'apps.todo.routes')
    """

    def include_routes(self, path, router):
        if not path.startswith('/'):
            raise ValueError('path should be started with /')
        elif path.endswith('/'):
            raise ValueError('path should not be ended with /')

        router = import_string('{}.router'.format(router))

        # include `resources`
        self._resources.extend(self._to_include(path, *router._resources))

        # include `named_resources`
        for name, resource in router._named_resources.items():
            if name in self._named_resources:
                raise ValueError('Duplicate {!r}, '
                                 'already handled by {!r}'
                                 .format(name, self._named_resources[name]))

            self._named_resources[name] = resource

    def _to_include(self, path, *resources):
        for resource in resources:
            if isinstance(resource, web_urldispatcher.PlainResource):
                resource._path = '{}{}'.format(path, resource._path)
            elif isinstance(resource, web_urldispatcher.DynamicResource):
                resource._pattern, resource._formatter = self._compile_path(
                    '{}{}'.format(path, resource._formatter))

        return resources

    def _compile_path(self, path):
        pattern = ''
        formatter = ''
        for part in self.ROUTE_RE.split(path):
            match = self.DYN.match(part)
            if match:
                pattern += '(?P<{}>{})'.format(match.group('var'), self.GOOD)
                formatter += '{' + match.group('var') + '}'
                continue

            match = self.DYN_WITH_RE.match(part)
            if match:
                pattern += '(?P<{var}>{re})'.format(**match.groupdict())
                formatter += '{' + match.group('var') + '}'
                continue

            if '{' in part or '}' in part:
                raise ValueError("Invalid path '{}'['{}']".format(path, part))

            formatter += part
            pattern += re.escape(part)

        try:
            compiled = re.compile('^' + pattern + '$')
        except re.error as exc:
            raise ValueError(
                "Bad pattern '{}': {}".format(pattern, exc)) from None

        return compiled, formatter
