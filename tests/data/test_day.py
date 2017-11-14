# coding=utf-8

import unittest
import numpy as np
import pandas as pd
import sixquant as sq


class TestMethods(unittest.TestCase):
    def test_get_day_base_fields(self):
        # 1. 传入一个code、单日date、一个field，返回一个数据，数据类型为 np.float64
        data = sq.get_day('000001', date='2017-11-01', fields='close')
        self.assertTrue(isinstance(data, np.float64))
        self.assertEqual(11.4, data)

        # 2. 传入一个code、单日date、多个field，返回一行数据，数据类型为 Pandas Series
        data = sq.get_day('000001', date='2017-11-01', fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual({'open': 11.56, 'close': 11.4}, data.to_dict())

        # 3. 传入一个code、多日date、一个field，返回一列数据，数据类型为 Pandas Series
        data = sq.get_day('000001', start_date='2017-11-01', end_date='2017-11-02', fields='close')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual(['2017-11-01', '2017-11-02'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([11.4, 11.54], data.values.tolist())

        # 4. 传入一个code、多日date、多个field，返回一列数据，数据类型为 Pandas DataFrame
        data = sq.get_day('000001', start_date='2017-11-01', end_date='2017-11-02', fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(2, len(data))
        self.assertEqual(['2017-11-01', '2017-11-02'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([[11.56, 11.4], [11.36, 11.54]], data.values.tolist())

        # --------

        # 5. 传入多个code、单日date、一个field，返回一列数据，数据类型为 Pandas Series
        data = sq.get_day(['000001', '000002'], date='2017-11-01', fields='close')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual({'000001': 11.4, '000002': 29.15}, data.to_dict())

        # 6. 传入多个code、单日date、多个field，返回多行数据，数据类型为 Pandas DataFrame
        data = sq.get_day(['000001', '000002'], date='2017-11-01', fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(2, len(data))
        self.assertEqual(['000001', '000002'], data.index.tolist())
        self.assertEqual([[11.56, 11.4], [28.96, 29.15]], data.values.tolist())

        # 7. 传入多个code、多日date、一个field，返回多行数据，数据类型为 Pandas DataFrame
        data = sq.get_day(['000001', '000002'], start_date='2017-11-01', end_date='2017-11-02', fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(4, len(data))
        self.assertEqual(['2017-11-01', '2017-11-01', '2017-11-02', '2017-11-02'],
                         data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.4], ['000002', 29.15], ['000001', 11.54], ['000002', 29.45]],
                         data.values.tolist())

        # 8. 传入多个code、多日date、多个field，返回多行数据，数据类型为 Pandas DataFrame
        data = sq.get_day(['000001', '000002'], start_date='2017-11-01', end_date='2017-11-02',
                          fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(4, len(data))
        self.assertEqual(['2017-11-01', '2017-11-01', '2017-11-02', '2017-11-02'],
                         data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56, 11.4],
                          ['000002', 28.96, 29.15],
                          ['000001', 11.36, 11.54],
                          ['000002', 29.3, 29.45]], data.values.tolist())

        # --------

        # 因为有可能股票个数是动态变化的，希望处理结果时统一处理
        # 因此 '000001' 和['000001'] 是不同的，前者表示单个股票，后者表示多个股票

        # 5. 传入多个code、单日date、一个field，返回一列数据，数据类型为 Pandas Series
        data = sq.get_day(['000001'], date='2017-11-01', fields='close')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(1, len(data))
        self.assertEqual({'000001': 11.4}, data.to_dict())

        # 6. 传入多个code、单日date、多个field，返回多行数据，数据类型为 Pandas DataFrame
        data = sq.get_day(['000001'], date='2017-11-01', fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(1, len(data))
        self.assertEqual(['000001'], data.index.tolist())
        self.assertEqual([[11.56, 11.4]], data.values.tolist())

        # 7. 传入多个code、多日date、一个field，返回多行数据，数据类型为 Pandas DataFrame
        data = sq.get_day(['000001'], start_date='2017-11-01', end_date='2017-11-02', fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(2, len(data))
        self.assertEqual(['2017-11-01', '2017-11-02'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.4], ['000001', 11.54]],
                         data.values.tolist())

        # 8. 传入多个code、多日date、多个field，返回多行数据，数据类型为 Pandas DataFrame
        data = sq.get_day(['000001'], start_date='2017-11-01', end_date='2017-11-02',
                          fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(2, len(data))
        self.assertEqual(['2017-11-01', '2017-11-02'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56, 11.4], ['000001', 11.36, 11.54]], data.values.tolist())

    def test_get_day_backs(self):
        # 1. 数据缓存，中间有停牌数据直接丢弃
        # '000001' 2017-10-30 2017-10-31 2017-11-01
        # '600469' 2017-10-27 2017-10-30 2017-11-01 中间有停牌，丢弃
        data = sq.get_day(['000001', '600469'], date='2017-11-01', backs=2, drop_suspended=True, fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(3, len(data))
        self.assertEqual(['2017-10-30', '2017-10-31', '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56], ['000001', 11.54], ['000001', 11.4]], data.values.tolist())

        # '000001' 2017-10-30 2017-10-31 2017-11-01
        # '600469' 2017-10-29 2017-10-30 2017-11-01 中间有停牌，需要从补足

        # 2. 数据缓存，补足数据从缓存中获取
        sq.cache.reset_day_cache()
        sq.get_day(['000001'], start_date='2017-10-27', end_date='2017-11-01', fields='close')

        data = sq.get_day(['000001', '600469'], date='2017-11-01', backs=2, fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(6, len(data))
        self.assertEqual(['2017-10-30',
                          '2017-10-31',
                          '2017-11-01',
                          '2017-10-27',
                          '2017-10-30',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56],
                          ['000001', 11.54],
                          ['000001', 11.4],
                          ['600469', 8.11],
                          ['600469', 7.98],
                          ['600469', 7.44]], data.values.tolist())

        # 3. 清空缓存，补足数据从数据库中获取
        sq.cache.reset_day_cache()
        data = sq.get_day(['000001', '600469'], date='2017-11-01', backs=2, fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(6, len(data))
        self.assertEqual(['2017-10-30',
                          '2017-10-31',
                          '2017-11-01',
                          '2017-10-27',
                          '2017-10-30',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56],
                          ['000001', 11.54],
                          ['000001', 11.4],
                          ['600469', 8.11],
                          ['600469', 7.98],
                          ['600469', 7.44]], data.values.tolist())

    def test_get_day_filed_name_translate(self):
        self.assertEqual(11.4, sq.get_day('000001', date='2017-11-01', fields='close'))

        self.assertEqual(11.54, sq.get_day('000001', date='2017-11-01', fields='prev_close'))
        self.assertEqual(11.54, sq.get_day('000001', date='2017-11-01', fields='prev_price'))

        self.assertEqual(-1.21, sq.get_day('000001', date='2017-11-01', fields='pt_close'))
        self.assertEqual(-1.21, sq.get_day('000001', date='2017-11-01', fields='pt_price'))

        self.assertEqual(792881043.0, sq.get_day('000001', date='2017-11-01', fields='money'))
        self.assertEqual(792881043.0, sq.get_day('000001', date='2017-11-01', fields='amount'))

    def test_get_day_dynamic_filed(self):
        # 昨日收盘价
        data = sq.get_day('000001', date='2017-11-01', fields='prev_price')
        self.assertEqual(11.54, data)

        # 涨幅
        data = sq.get_day('000001', date='2017-11-01', fields='pt_price')
        self.assertEqual(-1.21, data)

        data = sq.get_day('000001', date='2017-11-01', fields=['prev_price', 'close'])
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual({'prev_price': 11.54, 'close': 11.4}, data.to_dict())

        # 震幅
        data = sq.get_day('000001', date='2017-11-01', fields='pt_ampl')
        self.assertEqual(2.34, data)

        data = sq.get_day('000001', date='2017-11-01', fields=['close', 'pt_ampl'])
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual({'close': 11.4, 'pt_ampl': 2.34}, data.to_dict())


if __name__ == '__main__':
    if not sq.option.is_development_env():
        sq.daily_updater.update_bundle('2017-10-27')
        sq.daily_updater.update_bundle('2017-10-30')
        sq.daily_updater.update_bundle('2017-11-01')
        sq.daily_updater.update_bundle('2017-11-02')

    unittest.main()
