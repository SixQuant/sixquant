# coding=utf-8

import unittest

from sixquant import append_if_not_exists


class TestMethods(unittest.TestCase):
    def test_append_if_not_exists(self):
        """Test :func:`append_if_not_exists()`."""
        self.assertEqual(None, append_if_not_exists(None, None))
        self.assertListEqual([], append_if_not_exists([], None))
        self.assertListEqual([], append_if_not_exists([], []))
        self.assertListEqual([1], append_if_not_exists([], [1]))
        self.assertListEqual([1], append_if_not_exists(None, [1]))
        self.assertListEqual([1], append_if_not_exists([1], [1]))
        self.assertListEqual([1, 2], append_if_not_exists([1], 2))
        self.assertListEqual([1, 2, 3], append_if_not_exists([1, 2], [1, 3]))
        self.assertListEqual([None, 1], append_if_not_exists([None], [1, None]))

        self.assertEqual({'name': 1}, append_if_not_exists({'name': 1}, 2))


if __name__ == '__main__':
    unittest.main()
