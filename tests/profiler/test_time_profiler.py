# coding=utf-8

import unittest

from sixquant import TimeProfiler


class TestMethods(unittest.TestCase):
    def test_time_profiler(self):
        with TimeProfiler():
            pass

        with TimeProfiler(verbose=True):
            pass

        with TimeProfiler(verbose=False):
            pass

        with TimeProfiler('abc', True):
            pass

        with TimeProfiler('abc', False):
            pass


if __name__ == '__main__':
    unittest.main()
