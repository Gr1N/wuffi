# -*- coding: utf-8 -*-

import json
from http import HTTPStatus

from aiohttp import web

__all__ = (
    'ValidationMixin',
    'ValidationView',
)


class ValidationMixin(object):
    validator_class = None
    validation_schema = None

    def get_validator_class(self):
        """
        Returns the validator class to use in this view.
        """
        return self.validator_class

    def get_validator(self):
        """
        Returns an instance of the validator to be used in this view.
        """
        return self.get_validator_class()(**self.get_validator_kwargs())

    def get_validator_kwargs(self):
        """
        Returns the keyword arguments for instantiating the validator.
        """
        return {
            'schema': self.get_validation_schema(),
        }

    def get_validation_schema(self):
        """
        Returns validation schema to use in this view.
        """
        return self.validation_schema

    async def get_document(self):
        """
        Returns document to validate in this view.
        """
        try:
            document = await self.request.json()
        except json.JSONDecodeError:
            document = {}

        return document

    async def document_valid(self, document):
        """
        If the document is valid, return `OK` response.
        """
        return web.json_response()

    async def document_invalid(self, document, errors):
        """
        If the document is not valid, return `BAD_REQUEST` response
        with errors dictionary.
        """
        return web.json_response(data=errors, status=HTTPStatus.BAD_REQUEST)


class ValidationView(ValidationMixin,
                     web.View):
    """
    A base view for processing POST requests which requires data validation.
    """
    async def post(self):
        """
        Handles POST requests, instantiating a validator instance with the
        passed validation scheme and then checked passed document for validity.
        """
        v = self.get_validator()
        d = await self.get_document()

        if not v.validate(d):
            return await self.document_invalid(v.document, v.errors)

        return await self.document_valid(v.document)
