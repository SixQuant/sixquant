# coding=utf-8

import unittest
import datetime
from sixquant import to_date_object, to_date_str, to_date_str_short, is_trading_time, is_trading_day, \
    is_trading_day_today, is_trading_time_now


class TestMethods(unittest.TestCase):
    def test_to_date_object(self):
        """Test :func:`to_date_object()`."""
        self.assertEqual(None, to_date_object(None))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('20120305').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('2012-03-05').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('03-05-2012').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('2012/03/05').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('03/05/2012').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 16:26:23', to_date_object('2012-03-05 16:26:23') \
                         .strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 16:26:23',
                         to_date_object(datetime.datetime.strptime('2012-03-05 16:26:23', '%Y-%m-%d %H:%M:%S')) \
                         .strftime('%Y-%m-%d %H:%M:%S'))

    def test_to_date_str(self):
        """Test :func:`to_date_str()`."""
        self.assertEqual('', to_date_str(None))
        self.assertEqual('2012-03-05', to_date_str(to_date_object('2012-03-05')))

    def test_to_date_str_short(self):
        """Test :func:`to_date_str()`."""
        self.assertEqual('', to_date_str_short(None))
        self.assertEqual('20120305', to_date_str_short(to_date_object('2012-03-05')))

    def test_is_trading_day(self):
        """Test :func:`is_trading_day()`."""
        self.assertFalse(is_trading_day('2017-10-05'))
        self.assertTrue(is_trading_day('2017-10-09'))
        self.assertEqual(is_trading_day(datetime.date.today()), is_trading_day_today())

    def test_is_trading_time(self):
        """Test :func:`is_trading_time()`."""
        self.assertFalse(is_trading_time('2017-10-05 10:00:00'))
        self.assertEqual(is_trading_time(datetime.datetime.now()), is_trading_time_now())


if __name__ == '__main__':
    unittest.main()
