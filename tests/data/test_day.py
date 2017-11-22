# coding=utf-8

import unittest
import numpy as np
import pandas as pd
import sixquant as sq
from sixquant.data.day import _calc_prev_close


class TestMethods(unittest.TestCase):
    def setUp(self):
        if not sq.option.is_development_env():
            sq.daily_updater.update_bundle('2017-10-26')
            sq.daily_updater.update_bundle('2017-10-27')
            sq.daily_updater.update_bundle('2017-10-30')
            sq.daily_updater.update_bundle('2017-10-31')
            sq.daily_updater.update_bundle('2017-11-01')
            sq.daily_updater.update_bundle('2017-11-02')

    def test_get_day_argument(self):
        """测试错误参数"""
        try:
            sq.get_day('000001', date='2017-11-01', end_date='2017-11-01')
            self.assertTrue(False)
        except sq.IllegalArgumentError:
            pass

        try:
            sq.get_day('000001', adjust_type='None')
            self.assertTrue(False)
        except Exception:
            pass

    def test_get_day_empty(self):
        """测试数据不存在"""

        self.assertEqual(None, sq.get_day('001', date='2017-10-31', fields='price'))
        self.assertEqual(None, sq.get_day('001', date='2017-10-31', fields='pt_close'))

        self.assertEqual(None, sq.get_day('600469', date='2017-10-31', fields='close'))
        self.assertEqual(None, sq.get_day('600469', date='2017-10-31', fields=['open', 'close']))
        self.assertEqual(None, sq.get_day(['600469'], date='2017-10-31', fields='close'))

        data = sq.get_day(['600469'], date='2017-10-31', fields=['open', 'close'])
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(0, len(data))
        self.assertEqual(['open', 'close'], data.columns.tolist())

    def test_get_day_base_fields(self):
        """测试基本字段"""

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

    def test_get_day_start_date(self):
        """测试开始日期模式"""

        # '000001' 2017-10-30 2017-10-31 2017-11-01
        # '600469' 2017-10-27 2017-10-30 2017-11-01 中间有停牌

        # 2. 中间有停牌数据的不做其他处理
        data = sq.get_day(['000001', '600469'], start_date='2017-10-30', end_date='2017-11-01', fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(5, len(data))
        self.assertEqual(['2017-10-30',
                          '2017-10-30',
                          '2017-10-31',
                          '2017-11-01',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56],
                          ['600469', 7.98],
                          ['000001', 11.54],
                          ['000001', 11.4],
                          ['600469', 7.44]], data.values.tolist())

        # 2. 中间有停牌数据的直接丢弃该股票全部数据 drop_suspended=True
        data = sq.get_day(['000001', '600469'], start_date='2017-10-30', end_date='2017-11-01', fields='close',
                          drop_suspended=True)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(3, len(data))
        self.assertEqual(['2017-10-30', '2017-10-31', '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56], ['000001', 11.54], ['000001', 11.4]], data.values.tolist())

    def test_get_day_backs(self):
        """测试回溯模式"""

        # '000001' 2017-10-30 2017-10-31 2017-11-01
        # '600469' 2017-10-27 2017-10-30 2017-11-01 中间有停牌

        # 1. 中间有停牌数据的直接丢弃该股票全部数据 drop_suspended=True
        data = sq.get_day(['000001', '600469'], date='2017-11-01', backs=2, drop_suspended=True, fields='close')
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(3, len(data))
        self.assertEqual(['2017-10-30', '2017-10-31', '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 11.56], ['000001', 11.54], ['000001', 11.4]], data.values.tolist())

        # 2. 中间有停牌数据的往前回溯补足数据个数（数据从缓存中获取）
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

        # 3. 中间有停牌数据的往前回溯补足数据个数（数据从数据库中获取）
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

    def test__calc_prev_close(self):
        """"计算昨日价格辅助函数"""

        data = pd.DataFrame(
            [['2017-10-31', 1],
             ['2017-11-01', 2]
             ], columns=['date', 'close']
        )
        data.date = pd.to_datetime(data.date)
        data.set_index('date', inplace=True)
        data = _calc_prev_close(data)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(1, len(data))
        self.assertEqual(['2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([[2, 1.0]], data.values.tolist())

        data = pd.DataFrame(
            [['2017-10-31', '000001', 1],
             ['2017-10-31', '000002', 3],
             ['2017-11-01', '000001', 2],
             ['2017-11-01', '000002', 5]
             ], columns=['date', 'code', 'close']
        )
        data.date = pd.to_datetime(data.date)
        data.set_index('date', inplace=True)
        data = _calc_prev_close(data)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(2, len(data))
        self.assertEqual(['2017-11-01', '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 2, 1.0], ['000002', 5, 3.0]], data.values.tolist())

        data = pd.DataFrame(
            [['2017-10-30', '000001', 0],
             ['2017-10-31', '000001', 1],
             ['2017-10-31', '000002', 3],
             ['2017-11-01', '000001', 2],
             ['2017-11-01', '000002', 5]
             ], columns=['date', 'code', 'close']
        )
        data.date = pd.to_datetime(data.date)
        data.set_index('date', inplace=True)
        data = _calc_prev_close(data)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(3, len(data))
        self.assertEqual(['2017-10-31', '2017-11-01', '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 1, 0.0], ['000001', 2, 1.0], ['000002', 5, 3.0]], data.values.tolist())

    def test_get_day_dynamic_fields(self):
        """"测试动态字段"""

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

    def test_get_day_dynamic_fields_complex(self):
        """"测试动态字段"""

        # 单个股票，单日，单字段
        data = sq.get_day('000001', date='2017-11-01', fields='pt_price')
        self.assertEqual(-1.21, data)

        data = sq.get_day('000002', date='2017-11-01', fields='pt_price')
        self.assertEqual(0.66, data)

        # 多个股票，单日，单字段
        data = sq.get_day(['000001', '000002'], date='2017-11-01', fields='pt_price')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual({'000001': -1.21, '000002': 0.66}, data.to_dict())

        # 单个股票，多日(回溯模式)，单字段
        # '000001' 2017-10-30 2017-10-31 2017-11-01
        # '600469' 2017-10-27 2017-10-30 2017-11-01 中间有停牌

        data = sq.get_day('000001', date='2017-11-01', backs=2, fields='pt_price')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(3, len(data))
        self.assertEqual(['2017-10-30',
                          '2017-10-31',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([0.0, -0.17, -1.21], data.values.tolist())

        data = sq.get_day('600469', date='2017-11-01', backs=2, fields='pt_price')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(3, len(data))
        self.assertEqual(['2017-10-27',
                          '2017-10-30',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([-0.86, -1.6, -6.77], data.values.tolist())

        data = sq.get_day('600469', start_date='2017-10-30', end_date='2017-11-01', fields='pt_price')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual(['2017-10-30',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([-1.6, -6.77], data.values.tolist())

    def test_get_day_filed_alias(self):
        """测试字段别名"""
        self.assertEqual(11.4, sq.get_day('000001', date='2017-11-01', fields='close'))
        self.assertEqual(11.4, sq.get_day('000001', date='2017-11-01', fields='price'))

        self.assertEqual(11.54, sq.get_day('000001', date='2017-11-01', fields='prev_close'))
        self.assertEqual(11.54, sq.get_day('000001', date='2017-11-01', fields='prev_price'))

        self.assertEqual(-1.21, sq.get_day('000001', date='2017-11-01', fields='pt_close'))
        self.assertEqual(-1.21, sq.get_day('000001', date='2017-11-01', fields='pt_price'))

        self.assertEqual(792881043.0, sq.get_day('000001', date='2017-11-01', fields='money'))
        self.assertEqual(792881043.0, sq.get_day('000001', date='2017-11-01', fields='amount'))

    def test_get_day_heat(self):
        data = sq.get_day_heat('000001', date='2017-11-01')
        self.assertEqual(-1.21, data)

        data = sq.get_day_heat(['000001', '000002'], date='2017-11-01')
        self.assertTrue(isinstance(data, pd.Series))
        self.assertEqual(2, len(data))
        self.assertEqual('heat', data.name)
        self.assertEqual({'000001': -1.21, '000002': 0.66}, data.to_dict())

        data = sq.get_day_heat(['000001', '000002'], date='2017-11-01', backs=2)
        self.assertTrue(isinstance(data, pd.DataFrame))
        self.assertEqual(6, len(data))
        self.assertEqual(['2017-10-30',
                          '2017-10-30',
                          '2017-10-31',
                          '2017-10-31',
                          '2017-11-01',
                          '2017-11-01'], data.index.strftime('%Y-%m-%d').tolist())
        self.assertEqual([['000001', 0.0],
                          ['000002', 5.38],
                          ['000001', -0.17],
                          ['000002', -0.07],
                          ['000001', -1.21],
                          ['000002', 0.66]], data.values.tolist())


if __name__ == '__main__':
    unittest.main()
