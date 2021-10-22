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
        prefixed_attributedict = {}
        for name, value in attributedict.items():
            if name.startswith('__') and name.endswith('__'):
                prefixed_attributedict[name] = value
            else:
                prefixed_attributedict[CustomMeta._prefix_name + name] = value

        return type.__new__(cls, clsname, superclasses, prefixed_attributedict)

    def __call__(cls, *args, **kwargs):
        base_setattr = cls.__setattr__
        cls.__setattr__ = CustomMeta.decorate_setattr(cls.__setattr__)
        self = super(CustomMeta, cls).__call__(*args, **kwargs)
        cls.__setattr__ = base_setattr

        return self

    @staticmethod
    #pylint: disable=W0622
    def decorate_setattr(setattr) -> Any:
        """
        Wrap __setattr__ method from base class in order to pad all attributes with prefix
        """
        @wraps(setattr)
        def wrapper(self, name, value):
            if name.startswith('__') and name.endswith('__'):
                return setattr(self, name, value)
            return setattr(self, CustomMeta._prefix_name + name, value)

        # pylint: disable=W0212
        wrapper._decorator_name_ = 'CustomMeta.decorate_setattr'
        return wrapper
