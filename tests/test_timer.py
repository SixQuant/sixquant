# coding=utf-8

import os
import sys
import unittest

from sixquant import fmt_round_number, fmt_file_size, Timer

root = os.path.abspath(os.path.expanduser(__file__ + '/../..'))
sys.path.append(root)


class TestMethods(unittest.TestCase):
    def test_timer(self):
        def nothing():
            pass

        #timer = Timer(interval=1, callback=nothing, async=False, daemon=False)
        #self.assertIsNotNone(timer.start())

        #timer = Timer(interval=1, callback=nothing, async=True, daemon=False)
        #self.assertIsNotNone(timer.start())
        #timer.stop()


if __name__ == '__main__':
    unittest.main()
