# coding=utf-8

import unittest
from sixquant import get_stocks, get_stock_name, get_stock_pe, get_stock_circulation, get_stock_circulation_cap, \
    get_launch_date, daily_cache

from sixquant import to_date_str
from sixquant import translate_stock_code


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
        daily_cache.set('basics', [])
        df = get_stocks()
        self.assertEqual(0, len(df))
        daily_cache.set('basics', None)

        self.assertIsNotNone(get_stocks())
        self.assertIsNotNone(get_stocks(small_only=True))
        self.assertIsNotNone(get_stocks(st_only=True))
        self.assertIsNotNone(get_stocks(subnew_only=True))
        self.assertIsNotNone(get_stocks(no_st=True))
        self.assertIsNotNone(get_stocks(no_subnew=True))

    def test_get_launch_date(self):
        self.assertEqual('1991-04-03', to_date_str(get_launch_date('000001')))
        df = get_launch_date(['000001', '000002'])
        self.assertEqual('1991-04-03', to_date_str(df.values[0]))
        self.assertEqual('1991-01-29', to_date_str(df.values[1]))

    def test_translate_stock_code(self):
        self.assertEqual(None, translate_stock_code(None))
        self.assertEqual('000001', translate_stock_code('000001'))
        self.assertEqual('IDX.000001', translate_stock_code('上证指数'))
        self.assertEqual('IDX.399001', translate_stock_code('深证成指'))
        self.assertEqual('IDX.399006', translate_stock_code('创业板指'))
        self.assertEqual('IDX.000016', translate_stock_code('上证50'))
        self.assertEqual('IDX.000300', translate_stock_code('沪深300'))

        self.assertListEqual(['000001', 'IDX.000001'], translate_stock_code(['000001', '上证指数']))


if __name__ == '__main__':
    unittest.main()
