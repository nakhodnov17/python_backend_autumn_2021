"""
custom_meta
=====

Provides
  1. Metaclass that add prefix to all attributes
"""

from typing import Any
from functools import wraps


class CustomMeta(type):
    """
    Metaclass that add prefix to all attributes
    """

    _prefix_name = 'custom_'

    def __new__(cls, clsname, superclasses, attributedict):
        obj = type.__new__(cls, clsname, superclasses, attributedict)
        obj.__getattribute__ = CustomMeta.decorate_getattribute(clsname, obj.__getattribute__)

        return obj

    @staticmethod
    def decorate_getattribute(clsname, getattribute) -> Any:
        """
        Wrap __getattribute__ method from base class in order to pad all attributes with prefix
        """
        @wraps(getattribute)
        def wrapper(self, name):
            if name.startswith('__') and name.endswith('__'):
                return getattribute(self, name)

            if name.startswith(CustomMeta._prefix_name):
                base_name = name[len(CustomMeta._prefix_name):]
                return getattribute(self, base_name)

            raise AttributeError(f"AttributeError: '{clsname}' object has no attribute '{name}'")

        # pylint: disable=W0212
        wrapper._decorator_name_ = 'CustomMeta.decorate_getattribute'
        return wrapper
