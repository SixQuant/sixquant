# coding=utf-8

import time

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
                print('%s elapsed time: %f ms' % (self.name, self.msecs))
            else:
                print('elapsed time: %f ms' % self.msecs)
