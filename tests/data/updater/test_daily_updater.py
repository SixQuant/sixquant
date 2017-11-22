# coding=utf-8

import unittest

from sixquant import get_last_trading_day
from sixquant.data.updater.daily_updater import daily_updater


class TestMethods(unittest.TestCase):
    #def test_update(self):
    #    daily_updater.update(get_last_trading_day())
    #    daily_updater.update()

    def test_update_bundle(self):
        exists, _ = daily_updater.update_bundle('2017-10-01')
        self.assertFalse(exists)
        exists, _ = daily_updater.update_bundle('2017-11-01')
        self.assertTrue(exists)


if __name__ == '__main__':
    unittest.main()
