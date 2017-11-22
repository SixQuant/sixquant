# coding=utf-8

import unittest

from sixquant import option, daily_updater, cached_db_day, IllegalArgumentError


class TestMethods(unittest.TestCase):
    def setUp(self):
        if not option.is_development_env():
            daily_updater.update_bundle('2017-10-30')
            daily_updater.update_bundle('2017-10-31')
            daily_updater.update_bundle('2017-11-01')
            daily_updater.update_bundle('2017-11-02')

    def test_get_day(self):
        cached_db_day.reset()
        try:
            cached_db_day.get_day(code_or_codes=None, start_date=None, end_date=None, backs=0,
                                  drop_suspended=False,
                                  fields=None)
            self.assertTrue(False)
        except IllegalArgumentError:
            pass

        try:
            cached_db_day.get_day(code_or_codes=None, start_date=None, end_date='2017-11-01', backs=0,
                                  drop_suspended=False,
                                  fields=None)
            self.assertTrue(False)
        except IllegalArgumentError:
            pass

        option.enable_caching_day = False
        cached_db_day.get_day(code_or_codes='000001', start_date=None, end_date='2017-11-01', backs=1,
                              drop_suspended=False,
                              fields=None)
        option.enable_caching_day = True

        cached_db_day.reset()
        cached_db_day.get_day(code_or_codes='000001', start_date='2017-11-01', end_date='2017-11-01',
                              backs=0, drop_suspended=False, fields=['close'])
        cached_db_day.get_day(code_or_codes='000001', start_date='2017-10-30', end_date='2017-11-02',
                              backs=0, drop_suspended=False, fields=['close'])

        cached_db_day.get_day(code_or_codes='000001', start_date=None, end_date='2017-11-02',
                              backs=1, drop_suspended=False, fields=['close'])

    def test_get_day2(self):

        # '600469' 2017-10-27 2017-10-30 2017-11-01 中间有停牌
        cached_db_day.reset()
        cached_db_day.get_day(code_or_codes='600469', start_date='2017-10-30', end_date='2017-11-01',
                              backs=0, drop_suspended=False, fields=['close'])
        data = cached_db_day.get_day(code_or_codes='600469', start_date=None, end_date='2017-10-31',
                                     backs=1, drop_suspended=False, fields=['close'])
        self.assertIsNotNone(data)
        # 更多测试见 test_day.py


if __name__ == '__main__':
    unittest.main()
