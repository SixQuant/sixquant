# coding=utf-8

import os
import sys
import unittest

root = os.path.abspath(os.path.expanduser(__file__ + '/../tests'))
sys.path.append(root)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.discover('tests'))
    unittest.TextTestRunner().run(suite)
