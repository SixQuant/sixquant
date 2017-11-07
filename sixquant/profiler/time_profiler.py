# coding=utf-8

import time

from .memory_profiler import get_used_memory_size_str

"""
usage:
with TimeProfiler("Test", True):
    XXXX
"""


class TimeProfiler(object):
    def __init__(self, name=None, verbose=False):
        self.name = name
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            if self.name:
                print('%s used memory %s, elapsed time: %f ms' % (self.name, get_used_memory_size_str(), self.msecs))
            else:
                print('used memory %s, elapsed time: %f ms' % (get_used_memory_size_str(), self.msecs))
