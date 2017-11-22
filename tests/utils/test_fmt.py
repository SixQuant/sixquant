# coding=utf-8
import datetime
import unittest

import time

from sixquant import fmt_round_number, fmt_file_size, fmt_money, fmt_numpy_datetime64, to_datetime_str, to_time_object


class TestMethods(unittest.TestCase):
    def test_fmt_round_number(self):
        """Test :func:`fmt_round_number()`."""
        self.assertEqual('1', fmt_round_number(1))
        self.assertEqual('1', fmt_round_number(1.0))
        self.assertEqual('1.00', fmt_round_number(1, keep_width=True))
        self.assertEqual('3.14', fmt_round_number(3.141592653589793))

    def test_fmt_file_size(self):
        """Test :func:`fmt_file_size()`."""
        self.assertEqual('0', fmt_file_size(0))
        self.assertEqual('1', fmt_file_size(1))
        self.assertEqual('42', fmt_file_size(42))
        self.assertEqual('1K', fmt_file_size(1024 ** 1))
        self.assertEqual('1M', fmt_file_size(1024 ** 2))
        self.assertEqual('1G', fmt_file_size(1024 ** 3))
        self.assertEqual('1T', fmt_file_size(1024 ** 4))
        self.assertEqual('1P', fmt_file_size(1024 ** 5))
        self.assertEqual('45K', fmt_file_size(1024 * 45))
        self.assertEqual('2.9T', fmt_file_size(1024 ** 4 * 2.9))

    def test_fmt_money(self):
        """Test :func:`fmt_money()`."""
        self.assertEqual('', fmt_money(None))
        self.assertEqual('1', fmt_money(1))
        self.assertEqual('1000', fmt_money(1000))
        self.assertEqual('1万', fmt_money(10000))
        self.assertEqual('1百万', fmt_money(100 * 10000))
        self.assertEqual('1千万', fmt_money(1000 * 10000))
        self.assertEqual('1亿', fmt_money(10000 * 10000))

        self.assertEqual('1.23万', fmt_money(12340))
        self.assertEqual('1.23百万', fmt_money(123.4 * 10000))
        self.assertEqual('1.23千万', fmt_money(1234 * 10000))
        self.assertEqual('1.23亿', fmt_money(12340 * 10000))

    def test_fmt_numpy_datetime64(self):
        """Test :func:`fmt_numpy_datetime64()`."""
        self.assertEqual('', fmt_numpy_datetime64(None, '%Y-%m-%d %H:%M:%S'))
        import numpy as np
        x = np.datetime64('2002-06-28 08:00:00.000000000')
        date = to_datetime_str(to_time_object('2002-06-28 08:00:00') + datetime.timedelta(seconds=-time.timezone))
        self.assertEqual(date, fmt_numpy_datetime64(x, '%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    unittest.main()
