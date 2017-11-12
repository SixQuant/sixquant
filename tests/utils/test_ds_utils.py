# coding=utf-8

import unittest

from sixquant.utils.ds_utils import append_if_not_exists


class TestMethods(unittest.TestCase):
    def test_append_if_not_exists(self):
        self.assertEqual(None, append_if_not_exists(None, None))
        self.assertListEqual([], append_if_not_exists([], None))
        self.assertListEqual([], append_if_not_exists([], []))
        self.assertListEqual([1], append_if_not_exists([], [1]))
        self.assertListEqual([1], append_if_not_exists(None, [1]))
        self.assertListEqual([1], append_if_not_exists([1], [1]))
        self.assertListEqual([1, 2, 3], append_if_not_exists([1, 2], [1, 3]))
        self.assertListEqual([None, 1], append_if_not_exists([None], [1, None]))


if __name__ == '__main__':
    unittest.main()
