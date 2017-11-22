# coding=utf-8

import unittest
import datetime

import time

from sixquant import to_date_object, to_date_str, to_date_str_short, is_trading_time, is_trading_day, \
    is_trading_day_today, is_trading_time_now, get_delta_trade_day, get_prev_trade_day, get_next_trade_day, \
    get_last_trading_day, to_time_object, get_last_histrade_day, is_holiday_today, is_holiday, to_datetime_str, \
    month_delta, option, is_leap_year, is_same_day, is_same_or_later_day, get_trade_days


class TestMethods(unittest.TestCase):
    def test_to_date_object(self):
        """Test :func:`to_date_object()`."""
        self.assertEqual(None, to_date_object(None))

        self.assertEqual('2012-03-05 00:00:00', to_date_object('20120305').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('2012-03-05').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('03-05-2012').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('2012/03/05').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('03/05/2012').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_date_object('2012-03-05 16:26:23')
                         .strftime('%Y-%m-%d %H:%M:%S'))

        self.assertEqual('2017-11-19 00:00:00', to_date_object('Sun, 19 Nov 2017 01:12:02 GMT')
                         .strftime('%Y-%m-%d %H:%M:%S'))

        import numpy as np
        x = np.datetime64('2012-06-28 08:00:00.000000000')
        self.assertEqual('2012-06-28 00:00:00', to_date_object(x).strftime('%Y-%m-%d %H:%M:%S'))

        date = datetime.date(2012, 3, 5)
        self.assertEqual('2012-03-05 00:00:00', to_date_object(date).strftime('%Y-%m-%d %H:%M:%S'))

        date = datetime.datetime(2012, 3, 5, 1, 2, 3)
        self.assertEqual('2012-03-05 00:00:00', to_date_object(date).strftime('%Y-%m-%d %H:%M:%S'))

    def test_to_time_object(self):
        """Test :func:`to_time_object()`."""
        self.assertEqual(None, to_time_object(None))

        self.assertEqual('2012-03-05 00:00:00', to_time_object('20120305').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_time_object('2012-03-05').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_time_object('03-05-2012').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_time_object('2012/03/05').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 00:00:00', to_time_object('03/05/2012').strftime('%Y-%m-%d %H:%M:%S'))
        self.assertEqual('2012-03-05 16:26:23', to_time_object('2012-03-05 16:26:23')
                         .strftime('%Y-%m-%d %H:%M:%S'))

        date = to_datetime_str(to_time_object('2017-11-19 01:12:02') + datetime.timedelta(seconds=-time.timezone))
        self.assertEqual(date, to_time_object('Sun, 19 Nov 2017 01:12:02 GMT')
                         .strftime('%Y-%m-%d %H:%M:%S'))

        import numpy as np
        x = np.datetime64('2002-06-28 08:00:00.000000000')
        date = to_datetime_str(to_time_object('2002-06-28 08:00:00') + datetime.timedelta(seconds=-time.timezone))
        self.assertEqual(date, to_time_object(x).strftime('%Y-%m-%d %H:%M:%S'))

        date = datetime.date(2012, 3, 5)
        self.assertEqual('2012-03-05 00:00:00', to_time_object(date).strftime('%Y-%m-%d %H:%M:%S'))

        date = datetime.datetime(2012, 3, 5, 1, 2, 3)
        self.assertEqual('2012-03-05 01:02:03', to_time_object(date).strftime('%Y-%m-%d %H:%M:%S'))

        try:
            to_time_object(1.2)
        except TypeError:
            pass

    def test_to_date_str(self):
        """Test :func:`to_date_str()`."""
        self.assertEqual('', to_date_str(None))
        self.assertEqual('2012-03-05', to_date_str(to_date_object('2012-03-05')))

    def test_to_date_str_short(self):
        """Test :func:`to_date_str()`."""
        self.assertEqual('', to_date_str_short(None))
        self.assertEqual('20120305', to_date_str_short(to_date_object('2012-03-05')))

    def test_to_datetime_str(self):
        """Test :func:`to_date_str()`."""
        self.assertEqual('', to_datetime_str(None))
        self.assertEqual('2012-03-05 12:34:56', to_datetime_str(to_time_object('2012-03-05 12:34:56')))

    def test_is_trading_day(self):
        """Test :func:`is_trading_day()`."""
        self.assertFalse(is_trading_day('2017-10-05'))
        self.assertTrue(is_trading_day('2017-10-09'))
        self.assertEqual(is_trading_day(datetime.date.today()), is_trading_day_today())

    def test_is_trading_time(self):
        """Test :func:`is_trading_time()`."""
        option.is_trading_time_now = True
        self.assertTrue(is_trading_time_now())
        option.is_trading_time_now = None

        self.assertFalse(is_trading_time('2017-10-05 10:19:19'))

        self.assertFalse(is_trading_time('2017-11-17 09:19:19'))
        self.assertTrue(is_trading_time('2017-11-17 09:20:00'))
        self.assertTrue(is_trading_time('2017-11-17 10:00:00'))
        self.assertTrue(is_trading_time('2017-11-17 11:30:59'))
        self.assertFalse(is_trading_time('2017-11-17 11:31:00'))
        self.assertFalse(is_trading_time('2017-11-17 11:59:59'))
        self.assertTrue(is_trading_time('2017-11-17 13:00:00'))
        self.assertTrue(is_trading_time('2017-11-17 14:00:00'))
        self.assertTrue(is_trading_time('2017-11-17 15:00:59'))
        self.assertFalse(is_trading_time('2017-11-17 15:01:00'))
        self.assertFalse(is_trading_time('2017-11-17 16:00:00'))

        self.assertEqual(is_trading_time(datetime.datetime.now()), is_trading_time_now())

    def test_last_trading_day(self):
        """Test :func:`get_last_trading_day()`."""
        get_last_trading_day()

        date = '2017-10-05'
        self.assertEqual('2017-09-29', to_date_str(get_last_trading_day(date)))
        date = datetime.datetime(2017, 11, 17, 7, 59, 59)
        self.assertEqual('2017-11-16', to_date_str(get_last_trading_day(date)))
        date = datetime.datetime(2017, 11, 17, 8, 00, 00)
        self.assertEqual('2017-11-17', to_date_str(get_last_trading_day(date)))

    def test_last_histrade_day(self):
        """Test :func:`get_last_histrade_day()`."""
        get_last_histrade_day()

        date = datetime.datetime(2017, 11, 17, 15, 59, 59)
        self.assertEqual('2017-11-16', to_date_str(get_last_histrade_day(0, date)))
        date = datetime.datetime(2017, 11, 17, 15, 59, 59)
        self.assertEqual('2017-11-15', to_date_str(get_last_histrade_day(-1, date)))
        date = datetime.datetime(2017, 11, 17, 16, 00, 00)
        self.assertEqual('2017-11-16', to_date_str(get_last_histrade_day(-1, date)))

    def test_delta_trade_day(self):
        """Test :func:`delta_trade_day()`."""
        date = '2017-10-05'
        self.assertEqual('2017-10-05', to_date_str(get_delta_trade_day(date, 0)))
        self.assertEqual('2017-09-29', to_date_str(get_delta_trade_day(date, -1)))
        self.assertEqual('2017-10-09', to_date_str(get_delta_trade_day(date, +1)))
        self.assertEqual('2017-09-29', to_date_str(get_prev_trade_day(date)))
        self.assertEqual('2017-10-09', to_date_str(get_next_trade_day(date)))

        self.assertEqual('2017-09-28', to_date_str(get_delta_trade_day(date, -2)))
        self.assertEqual('2017-10-10', to_date_str(get_delta_trade_day(date, +2)))

    def test_get_trade_days(self):
        self.assertEqual(1, get_trade_days('2017-11-01', '2017-11-01'))
        self.assertEqual(2, get_trade_days('2017-10-31', '2017-11-01'))

        self.assertEqual(3, get_trade_days('2017-10-01', '2017-10-10'))

    def test_is_same_day(self):
        """Test :func:`is_same_day()`."""
        is_holiday_today()
        self.assertTrue(is_same_day('2017-10-05', '2017-10-05 12:12:12'))
        self.assertFalse(is_same_day('2017-10-05', '2017-10-06 12:12:12'))
        self.assertTrue(is_same_or_later_day('2017-10-05', '2017-10-06 12:12:12'))

    def test_is_holiday(self):
        """Test :func:`is_holiday()`."""
        is_holiday_today()
        self.assertTrue(is_holiday('2017-10-05'))
        self.assertTrue(is_holiday('2017-10-06'))
        self.assertFalse(is_holiday('2017-10-07'))

    def test_is_leap_year(self):
        """Test :func:`is_leap_year()`."""
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(2004))
        self.assertFalse(is_leap_year(2017))

    def test_month_delta(self):
        """Test :func:`month_delta()`."""
        is_holiday_today()
        self.assertEqual('2017-01-01', to_date_str(month_delta('2017-01-01', 0)))
        self.assertEqual('2017-02-01', to_date_str(month_delta('2017-01-01', +1)))
        self.assertEqual('2016-12-01', to_date_str(month_delta('2017-01-01', -1)))
        self.assertEqual('2016-11-01', to_date_str(month_delta('2017-01-01', -2)))
        self.assertEqual('2017-01-01', to_date_str(month_delta('2016-12-01', +1)))
        self.assertEqual('2017-02-01', to_date_str(month_delta('2016-12-01', +2)))
        self.assertEqual('2016-12-01', to_date_str(month_delta('2016-11-01', +1)))

        self.assertEqual('2017-02-28', to_date_str(month_delta('2017-03-31', -1)))
        self.assertEqual('2000-02-29', to_date_str(month_delta('2000-03-31', -1)))


if __name__ == '__main__':
    unittest.main()
