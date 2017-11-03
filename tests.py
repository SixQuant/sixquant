# coding=utf-8

import os
import sys
import unittest

root = os.path.abspath(os.path.expanduser(__file__ + '/../tests'))
sys.path.append(root)

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for file in os.listdir('tests'):
        if file.startswith('test_') and file.endswith('.py'):
            file = file[:len(file) - 3]
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(file))

    unittest.TextTestRunner().run(suite)
