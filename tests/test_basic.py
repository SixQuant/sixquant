# coding=utf-8

import unittest
from sixquant import get_stocks, get_stock_name, get_stock_pe, get_stock_circulation, get_stock_circulation_cap


class TestMethods(unittest.TestCase):

    def test_get_stock_name(self):
        self.assertEqual('平安银行', get_stock_name('000001'))

    def test_get_stock_pe(self):
        self.assertTrue(get_stock_pe('000001') > 0)

    def test_get_stock_circulation(self):
        self.assertTrue(get_stock_circulation('000001') > 0)

    def test_get_stock_circulation_cap(self):
        self.assertTrue(get_stock_circulation_cap('000001') > 0)

    def test_get_get_stocks(self):
        self.assertIsNotNone(get_stocks())
        self.assertIsNotNone(get_stocks(small_only=True))
        self.assertIsNotNone(get_stocks(st_only=True))
        self.assertIsNotNone(get_stocks(subnew_only=True))
        self.assertIsNotNone(get_stocks(no_st=True))
        self.assertIsNotNone(get_stocks(no_subnew=True))

if __name__ == '__main__':
    unittest.main()
