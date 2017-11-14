# coding=utf-8

import unittest
from sixquant import cache


class TestMethods(unittest.TestCase):
    def test_cache_reset(self):
        cache.reset()


if __name__ == '__main__':
    unittest.main()
