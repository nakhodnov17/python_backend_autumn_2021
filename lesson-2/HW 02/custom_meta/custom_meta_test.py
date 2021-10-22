# pylint: disable=C0114,C0115,C0116

import unittest

from custom_meta import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_global(self):
        # pylint: disable=R0903
        class TestClass(metaclass=CustomMeta):
            x, y = 1, 2
            custom_x = 3

        obj = TestClass()
        with self.assertRaises(AttributeError):
            # pylint: disable=W0104
            obj.y
        with self.assertRaises(AttributeError):
            # pylint: disable=E1101,W0104
            obj.custom_z
        self.assertEqual(obj.custom_x, 1)
        # pylint: disable=E1101
        self.assertEqual(obj.custom_y, 2)
        # pylint: disable=E1101
        self.assertEqual(obj.custom_custom_x, 3)

        obj.x = 10
        self.assertEqual(obj.x, 10)

    def test_function(self):
        class TestClass(metaclass=CustomMeta):
            # pylint: disable=R0201
            def regular_func(self):
                return 0

            @staticmethod
            # pylint: disable=R0201
            def static_func():
                return 1

            # pylint: disable=R0201
            def _protected_func(self):
                return 2

            # pylint: disable=R0201
            def __magic_func__(self):
                return 3

        obj = TestClass()
        with self.assertRaises(AttributeError):
            # pylint: disable=W0104
            obj.regular_func
        with self.assertRaises(AttributeError):
            # pylint: disable=W0104
            obj.static_func
        with self.assertRaises(AttributeError):
            # pylint: disable=W0104,W0212
            obj._protected_func
        with self.assertRaises(AttributeError):
            # pylint: disable=E1101,W0104
            obj.custom_missing_func

        # pylint: disable=E1101
        self.assertEqual(obj.custom_regular_func(), 0)
        # pylint: disable=E1101
        self.assertEqual(obj.custom_static_func(), 1)
        # pylint: disable=E1101
        self.assertEqual(obj.custom__protected_func(), 2)
        self.assertEqual(obj.__magic_func__(), 3)

    def test_variable(self):
        # pylint: disable=R0903
        class TestClass(metaclass=CustomMeta):
            # pylint: disable=C0103
            def __init__(self, x, y, custom_x):
                self.x = x
                self.y = y
                self.custom_x = custom_x
                self.__magic__ = 1010

        obj = TestClass(1, 2, 3)
        with self.assertRaises(AttributeError):
            # pylint: disable=W0104
            obj.y
        with self.assertRaises(AttributeError):
            # pylint: disable=E1101, W0104
            obj.custom_z
        self.assertEqual(obj.custom_x, 1)
        # pylint: disable=E1101
        self.assertEqual(obj.custom_y, 2)
        # pylint: disable=E1101
        self.assertEqual(obj.custom_custom_x, 3)
        self.assertEqual(obj.__magic__, 1010)


if __name__ == '__main__':
    unittest.main()
