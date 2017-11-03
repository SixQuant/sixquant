# coding=utf-8

import unittest
from sixquant import get_day_today_quote, get_day_today_money
from sixquant import get_day_today, get_day_today_small, get_day_today_small_no_st_no_subnew


class TestMethods(unittest.TestCase):
    def test_get_day_today_quote(self):
        self.assertIsNotNone(get_day_today_quote())

    def test_get_day_today_money(self):
        self.assertIsNotNone(get_day_today_money())

    def test_get_day_today(self):
        self.assertIsNotNone(get_day_today())
        self.assertIsNotNone(get_day_today(fields=['open', 'close'], subnew_only=True))
        self.assertIsNotNone(get_day_today_small())
        self.assertIsNotNone(get_day_today_small_no_st_no_subnew())


if __name__ == '__main__':
    unittest.main()
