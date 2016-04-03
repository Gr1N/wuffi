# -*- coding: utf-8 -*-

from cerberus import (
    Validator as _Validator,
    ValidationError,
    SchemaError,
)

__all__ = (
    'Validator',
    'ValidationError',
    'SchemaError',

    'to_upper',
    'to_lower',
)


class Validator(_Validator):
    """
    `Validator` class, built on the basis of `cerberus.Validator` class.

    Full `cerberus` documentation is available at http://python-cerberus.org/,
    use it to understand how to extend `Validator` class.

    Usage example:
        In [1]: from wuffi import validation

        In [2]: v = validation.Validator()

        In [3]: schema = {
           ...:     'name': {
           ...:         'type': 'string',
           ...:         'minlength': 10,
           ...:         'coerce': validation.to_upper,
           ...:     },
           ...: }

        In [4]: v.validate({
           ...:     'name': 'I am super hero',
           ...: }, schema=schema)
        Out[4]: True

        In [5]: v.document
        {'name': 'I AM SUPER HERO'}

    """

    def validate(self, *args, **kwargs):
        super(Validator, self).validate(*args, **kwargs)

        self.post_validate()

        return not bool(self._errors)

    def post_validate(self):
        """
        An hook for performing additional validation after schema validation
        is complete.
        """


# `coerce` functions


def to_upper(value):
    return value.upper()


def to_lower(value):
    return value.lower()
