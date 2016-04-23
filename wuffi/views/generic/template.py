# -*- coding: utf-8 -*-

from aiohttp import web
from aiohttp_jinja2 import render_template

__all__ = (
    'TemplateMixin',
    'TemplateView',
)


class TemplateMixin(object):
    """
    A mixin that can be used to render a template.
    """

    template_name = None
    template_context = None
    content_type = None

    def render_to_response(self, context=None):
        context = context or self.get_context_data()

        response = render_template(self.template_name, self.request, context)
        return response

    def get_context_data(self):
        return self.template_context or {}


class TemplateView(TemplateMixin,
                   web.View):
    """
    A view that renders a template.
    """

    async def get(self):
        return self.render_to_response()
