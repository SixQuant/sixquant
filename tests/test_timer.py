# coding=utf-8

import unittest
from sixquant import fmt_round_number, fmt_file_size, Timer


class TestMethods(unittest.TestCase):
    def test_timer(self):
        def nothing():
            pass

            # timer = Timer(interval=1, callback=nothing, async=False, daemon=False)
            # self.assertIsNotNone(timer.start())

            # timer = Timer(interval=1, callback=nothing, async=True, daemon=False)
            # self.assertIsNotNone(timer.start())
            # timer.stop()


if __name__ == '__main__':
    unittest.main()
