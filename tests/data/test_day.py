# coding=utf-8

import unittest
import sixquant as sq
from sixquant import get_day
from sixquant.data.updater.daily_updater import daily_updater


class TestMethods(unittest.TestCase):
    def test_get_day(self):
        """
        传入一个code，一个field，函数会返回 Pandas Series
        传入一个code，多个field，函数会返回 Pandas DataFrame
        传入多个code，一个field，函数会返回 Pandas DataFrame
        传入多个code，多个field，函数会返回 Pandas MultiIndex DataFrame
                                        df.loc['300315'].loc['2017-10-08':'2017-10-09']

        :return:
        """
        data = get_day('000001')
        self.assertIsNotNone(data)
        self.assertTrue("<class 'pandas.core.series.Series'>", str(type(data)))
        self.assertTrue(len(data) > 0)

        data = get_day('000001', fields='close', start_date='2017-11-02', end_date='2017-11-03')
        self.assertIsNotNone(data)
        self.assertTrue("<class 'pandas.core.series.Series'>", str(type(data)))
        self.assertEqual(2, len(data))
        self.assertListEqual([11.54, 11.39], data.tolist())

        data = get_day('000001', start_date='2017-11-01', end_date='2017-11-03')
        self.assertIsNotNone(data)
        self.assertTrue("<class 'pandas.core.frame.DataFrame'>", str(type(data)))
        self.assertEqual(3, len(data))
        self.assertListEqual([11.4, 11.54, 11.39], data['close'].tolist())

        data = get_day(['000001', '000002'], start_date='2017-11-01', end_date='2017-11-03')
        self.assertIsNotNone(data)
        self.assertTrue("<class 'pandas.core.frame.DataFrame'>", str(type(data)))
        self.assertEqual(6, len(data))
        self.assertListEqual([11.4, 29.15, 11.54, 29.45, 11.39, 28.19], data['close'].tolist())


daily_updater.update_bundle('2017-11-01')
daily_updater.update_bundle('2017-11-02')
daily_updater.update_bundle('2017-11-03')

if __name__ == '__main__':
    unittest.main()
