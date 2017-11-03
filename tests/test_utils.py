# coding=utf-8

import os
import sys
import unittest

root = os.path.abspath(os.path.expanduser(__file__ + '/../..'))
sys.path.append(root)

from sixquant import to_date_object, to_date_str, to_date_str_short
import datetime


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


if __name__ == '__main__':
    unittest.main()
