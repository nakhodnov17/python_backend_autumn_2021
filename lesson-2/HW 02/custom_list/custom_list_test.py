# pylint: disable=C0114,C0115,C0116

import unittest
import numpy as np

from custom_list import CustomList


class TestCustomList(unittest.TestCase):
    def test_creation(self):
        values = [1, 2, 3, 4]
        self.assertIsInstance(CustomList(values), list)
        self.assertIsInstance(CustomList(values), CustomList)

        self.assertListEqual(values, CustomList(values))

    def test_sub(self, seed=43):
        def _check(_left, _right):
            _left, _right = np.array(_left), np.array(_right)
            max_len = max(_left.shape[0], _right.shape[0])
            _left = np.pad(_left, (0, max_len - _left.shape[0]), 'constant', constant_values=(0, 0))
            _right = np.pad(_right, (0, max_len - _right.shape[0]), 'constant', constant_values=(0, 0))
            return (_left - _right).tolist()

        tests = [
            ([], CustomList([])),
            ([], CustomList([1])),
            ([], CustomList([1, 2, 3])),
            ([1], CustomList([])),
            ([1, 2], CustomList([])),
            ([1, 2, 3], CustomList([])),
            ([4, 5, 6], CustomList([1])),
            ([4, 5, 6], CustomList([1, 2, 3])),
            ([4, 5, 6], CustomList([1, 2, 3, 7, 8])),

            (CustomList([]), CustomList([])),
            (CustomList([]), CustomList([1])),
            (CustomList([]), CustomList([1, 2, 3])),
            (CustomList([1]), CustomList([])),
            (CustomList([1, 2]), CustomList([])),
            (CustomList([1, 2, 3]), CustomList([])),
            (CustomList([4, 5, 6]), CustomList([1])),
            (CustomList([4, 5, 6]), CustomList([1, 2, 3])),
            (CustomList([4, 5, 6]), CustomList([1, 2, 3, 7, 8])),
        ]

        random_generator = np.random.default_rng(seed)
        for _ in range(1000):
            left_len, right_len = random_generator.integers(0, 10, 2)
            left = random_generator.integers(-100, 100, left_len).tolist()
            right = random_generator.integers(-100, 100, right_len).tolist()
            tests.append((left, CustomList(right)))
            tests.append((CustomList(left), CustomList(right)))

        for left, right in tests:
            self.assertIsInstance(left - right, CustomList)
            self.assertListEqual(left - right, _check(left, right))

            self.assertIsInstance(right - left, CustomList)
            self.assertListEqual(right - left, _check(right, left))

    def test_add(self, seed=44):
        def _check(_left, _right):
            _left, _right = np.array(_left), np.array(_right)
            max_len = max(_left.shape[0], _right.shape[0])
            _left = np.pad(_left, (0, max_len - _left.shape[0]), 'constant', constant_values=(0, 0))
            _right = np.pad(_right, (0, max_len - _right.shape[0]), 'constant', constant_values=(0, 0))
            return (_left + _right).tolist()

        tests = [
            ([], CustomList([])),
            ([], CustomList([1])),
            ([], CustomList([1, 2, 3])),
            ([1], CustomList([])),
            ([1, 2], CustomList([])),
            ([1, 2, 3], CustomList([])),
            ([4, 5, 6], CustomList([1])),
            ([4, 5, 6], CustomList([1, 2, 3])),
            ([4, 5, 6], CustomList([1, 2, 3, 7, 8])),

            (CustomList([]), CustomList([])),
            (CustomList([]), CustomList([1])),
            (CustomList([]), CustomList([1, 2, 3])),
            (CustomList([1]), CustomList([])),
            (CustomList([1, 2]), CustomList([])),
            (CustomList([1, 2, 3]), CustomList([])),
            (CustomList([4, 5, 6]), CustomList([1])),
            (CustomList([4, 5, 6]), CustomList([1, 2, 3])),
            (CustomList([4, 5, 6]), CustomList([1, 2, 3, 7, 8])),
        ]

        random_generator = np.random.default_rng(seed)
        for _ in range(1000):
            left_len, right_len = random_generator.integers(0, 10, 2)
            left = random_generator.integers(-100, 100, left_len).tolist()
            right = random_generator.integers(-100, 100, right_len).tolist()
            tests.append((left, CustomList(right)))
            tests.append((CustomList(left), CustomList(right)))

        for left, right in tests:
            self.assertIsInstance(left + right, CustomList)
            self.assertListEqual(left + right, _check(left, right))

            self.assertIsInstance(right + left, CustomList)
            self.assertListEqual(right + left, _check(right, left))

    def test_comparation(self, seed=42):
        tests = [
            (0, [], CustomList([])),
            (0, [], CustomList([0])),
            (1, [], CustomList([-1])),
            (-1, [], CustomList([1])),
            (1, [], CustomList([1, -5, 3])),
            (0, [], CustomList([1, -5, 4])),
            (-1, [], CustomList([1, 2, 3])),
            (0, [5, -2, -3], CustomList([])),
            (1, [5, -2, 3], CustomList([])),
            (1, [5, -2, 3], CustomList([0])),
            (1, [5, -2, 3], CustomList([-1])),
            (-1, [5, -2, 3], CustomList([7])),
            (0, [5, -2, 3], CustomList([7, -1])),
            (1, [5, -2, 3], CustomList([1, -5, 3])),
            (1, [5, -2, 3], CustomList([1, -5, 9])),
            (-1, [5, -2, 3], CustomList([1, 2, 3, 4])),

            (0, CustomList([]), CustomList([])),
            (0, CustomList([]), CustomList([0])),
            (1, CustomList([]), CustomList([-1])),
            (-1, CustomList([]), CustomList([1])),
            (1, CustomList([]), CustomList([1, -5, 3])),
            (0, CustomList([]), CustomList([1, -5, 4])),
            (-1, CustomList([]), CustomList([1, 2, 3])),
            (0, CustomList([5, -2, -3]), CustomList([])),
            (1, CustomList([5, -2, 3]), CustomList([])),
            (1, CustomList([5, -2, 3]), CustomList([0])),
            (1, CustomList([5, -2, 3]), CustomList([-1])),
            (-1, CustomList([5, -2, 3]), CustomList([7])),
            (0, CustomList([5, -2, 3]), CustomList([7, -1])),
            (1, CustomList([5, -2, 3]), CustomList([1, -5, 3])),
            (1, CustomList([5, -2, 3]), CustomList([1, -5, 9])),
            (-1, CustomList([5, -2, 3]), CustomList([1, 2, 3, 4])),
        ]

        random_generator = np.random.default_rng(seed)
        for _ in range(1000):
            left_len, right_len = random_generator.integers(0, 10, 2)
            left = random_generator.integers(-100, 100, left_len).tolist()
            right = random_generator.integers(-100, 100, right_len).tolist()
            answer = 0 if sum(left) == sum(right) else (-1 if sum(left) < sum(right) else 1)
            tests.append((answer, left, CustomList(right)))
            tests.append((answer, CustomList(left), CustomList(right)))

        for result, left, right in tests:
            if result == 0:
                self.assertFalse(left < right, f'{left} < {right}')
                self.assertTrue(left <= right, f'{left} <= {right}')
                self.assertTrue(left == right, f'{left} == {right}')
                self.assertFalse(left != right, f'{left} != {right}')
                self.assertFalse(left > right, f'{left} > {right}')
                self.assertTrue(left >= right, f'{left} >= {right}')

                self.assertFalse(right < left, f'{right} < {left}')
                self.assertTrue(right <= left, f'{right} <= {left}')
                self.assertTrue(right == left, f'{right} == {left}')
                self.assertFalse(right != left, f'{right} != {left}')
                self.assertFalse(right > left, f'{right} > {left}')
                self.assertTrue(right >= left, f'{right} >= {left}')
            elif result == -1:
                self.assertTrue(left < right, f'{left} < {right}')
                self.assertTrue(left <= right, f'{left} <= {right}')
                self.assertFalse(left == right, f'{left} == {right}')
                self.assertTrue(left != right, f'{left} != {right}')
                self.assertFalse(left > right, f'{left} > {right}')
                self.assertFalse(left >= right, f'{left} >= {right}')

                self.assertFalse(right < left, f'{right} < {left}')
                self.assertFalse(right <= left, f'{right} <= {left}')
                self.assertFalse(right == left, f'{right} == {left}')
                self.assertTrue(right != left, f'{right} != {left}')
                self.assertTrue(right > left, f'{right} > {left}')
                self.assertTrue(right >= left, f'{right} >= {left}')
            elif result == 1:
                self.assertFalse(left < right, f'{left} < {right}')
                self.assertFalse(left <= right, f'{left} <= {right}')
                self.assertFalse(left == right, f'{left} == {right}')
                self.assertTrue(left != right, f'{left} != {right}')
                self.assertTrue(left > right, f'{left} > {right}')
                self.assertTrue(left >= right, f'{left} >= {right}')

                self.assertTrue(right < left, f'{right} < {left}')
                self.assertTrue(right <= left, f'{right} <= {left}')
                self.assertFalse(right == left, f'{right} == {left}')
                self.assertTrue(right != left, f'{right} != {left}')
                self.assertFalse(right > left, f'{right} > {left}')
                self.assertFalse(right >= left, f'{right} >= {left}')


if __name__ == '__main__':
    unittest.main()
