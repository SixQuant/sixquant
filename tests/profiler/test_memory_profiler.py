# coding=utf-8

import unittest

from sixquant import get_used_memory_size_str


class TestMethods(unittest.TestCase):
    def test_memory_profiler(self):
        get_used_memory_size_str()


if __name__ == '__main__':
    unittest.main()
