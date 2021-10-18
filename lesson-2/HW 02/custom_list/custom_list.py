"""
custom_list
=====

Provides
  1. List class with addition, subtraction and comparation
"""

from itertools import chain


class CustomList(list):
    """
    List class with additional operations -- addition, subtraction and comparation
    """

    def __spaceship(self, other):
        left_sum = sum(self)
        right_sum = sum(other)
        return left_sum - right_sum

    def __lt__(self, other):
        return self.__spaceship(other) < 0

    def __le__(self, other):
        return self.__spaceship(other) <= 0

    def __eq__(self, other):
        return self.__spaceship(other) == 0

    def __ne__(self, other):
        return self.__spaceship(other) != 0

    def __ge__(self, other):
        return self.__spaceship(other) >= 0

    def __gt__(self, other):
        return self.__spaceship(other) > 0

    def __add__(self, other):
        new_iterable = chain(
            (left + right for left, right in zip(self, other)),
            other[len(self):] if len(self) < len(other) else self[len(other):]
        )
        return CustomList(new_iterable)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return -(other + (-self))

    def __rsub__(self, other):
        return -self.__sub__(other)

    def __neg__(self):
        return CustomList((-value for value in self))
