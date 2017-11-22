# coding=utf-8

import pandas as pd

from ..utils.factor_utils import get_relevant_factor
from ..utils.exceptions import IllegalArgumentError
from ..utils.ds_utils import append_if_not_exists
from ..utils.field_name_translator import translate_field_name
from ..utils.datetime_utils import get_delta_trade_day, get_last_histrade_day, to_date_object, get_prev_trade_day
from .basic import translate_stock_code
from .database.cached_db_day import cached_db_day

"""
股票日线信息
"""


def _calc_prev_close(df):
    """
    计算昨日收盘价
    :param df:
    :return:
    """

    if 'code' not in df.columns:
        # 单个股票
        # 删除最早一天的数据
        # 计算早一天的收盘价
        df['prev_close'] = df['close'].shift(1)
        df = df.loc[df.index != df.index.min()]
    else:
        # 多个股票
        # 让数据按照 CODE,DATE 排序
        df.index.name = 'date'
        df.reset_index(inplace=True)
        df.sort_values(['code', 'date'], inplace=True)

        # 计算昨日收盘价
        df['prev_close'] = df['close'].shift(1)

        # 让数据恢复 DATE,CODE 排序
        df.sort_values(['date', 'code'], inplace=True)

        # 删除早一天的数据
        df = df.loc[~df.index.isin(df.groupby(['code'])['date'].idxmin())]

        df.set_index('date', inplace=True)
        df.index.name = ''

    return df


def get_day(code_or_codes,
            start_date=None,
            end_date=None,
            date=None,
            backs=0,
            drop_suspended=False,
            fields=None,
            adjust_type='pre'
            ):
    """
    得到股票日线数据

    Features
    ---------
    * 专为性能优化
    * 支持真正历史日期的复权数据
    * 支持字段兼容，可以使用不同的的字段名称表示同一个数据
    *

    Parameters
    ----------
    code_or_codes : str/str array
        单个股票代码或股票代码数组
    start_date : date str/date
        数据开始日期
        start_date 和 backs 同时出现时表示需要 start_date 前 backs 个数据
    end_date : date str/date
        数据结束日期
    date : date str/date
        等价于 end_date
        一般表示只取某一天的数据
        和 backs 参数配套使用时表示取某一天以及前 backs 个数据
    backs : int
        表示从 start_date 或 end_date/date 日期往前有 n 条记录，以便用来画图等
    drop_suspended : bool
        是否直接丢弃中间有停牌的数据
        和 backs 配套使用
    fields : str/str array
        单个字段名称或字段名称数组
    adjust_type : str
        复权类型 pre/None

    Notes
    -----
    请尽可能的用的时候取数据，而不是一次性取

    Returns
    -------
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
    # 因此 '000001' 和 ['000001'] 是不同的，前者表示单个股票，后者表示多个股票

    # 5. 传入多个code、单日date、一个field，返回一列数据，数据类型为 Pandas Series
    data = sq.get_day(['000001'], date='2017-11-01', fields='close')
    self.assertTrue(isinstance(data, pd.Series))
    self.assertEqual(1, len(data))
    self.assertEqual({'000001': 11.4}, data.to_dict())

    Examples
    --------
    df = sq.get_day('000001', date='2017-11-06', fields=['close', 'pt_price'])

    """
    # 参数检查
    if date is not None and end_date is not None:
        raise IllegalArgumentError('either end_date or date, not both!')

    # date 等价于 end_date
    if date is not None:
        end_date = date
        del date

    # 缺省参数处理
    if end_date is None:
        end_date = get_last_histrade_day(0)  # 默认取最后一个交易日
    else:
        end_date = to_date_object(end_date)

    if start_date is not None:
        start_date = to_date_object(start_date)

    if fields is None:
        fields = ['open', 'high', 'low', 'close', 'volume', 'amount']  # 全部基本字段
    elif isinstance(fields, str):
        fields = [fields]

    multiple_codes = not isinstance(code_or_codes, str)  # 是否同时取多个股票数据
    single_date = backs == 0 and (start_date is None or start_date == end_date)  # 是否单日数据
    single_fields = len(fields) == 1  # 是否单个字段数据

    if multiple_codes:
        fields = append_if_not_exists(['code'], fields)

    # 字段名称兼容转换
    original_fields = fields
    fields, filed_name_changed = translate_field_name(fields)

    fetch_fields = []  # 实际获取的数据字段

    if adjust_type == 'pre':
        fetch_fields.append('factor')  # 需要额外的字段用于计算复权

    fetch_fields = append_if_not_exists(fetch_fields, fields)

    # 动态计算字段处理

    dynamic_filed = False  # 是否有动态字段
    temp_fields = []

    prev_close_based_dynamic_fields = ['prev_close', 'pt_close', 'pt_ampl']  # 需要 close 字段的动态字段
    for label in prev_close_based_dynamic_fields:
        if label in fetch_fields:
            dynamic_filed = True
            if 'close' not in fields and 'close' not in temp_fields:
                temp_fields.append('close')  # 临时需要 close 字段数据
            if 'pt_ampl' == label:  # 临时需要 high、low 字段数据
                if 'high' not in fields and 'high' not in temp_fields:
                    temp_fields.append('high')
                if 'low' not in fields and 'low' not in temp_fields:
                    temp_fields.append('low')
            del fetch_fields[fetch_fields.index(label)]

    fetch_start_date = start_date if start_date is not None else end_date
    if dynamic_filed:  # 需要前一天的数据
        backs = backs + 1

    if len(temp_fields) > 0:
        fetch_fields = append_if_not_exists(fetch_fields, temp_fields)

    # 获取原始数据
    code_or_codes = translate_stock_code(code_or_codes)
    df = cached_db_day.get_day(code_or_codes=code_or_codes,
                               start_date=fetch_start_date,
                               end_date=end_date,
                               backs=backs,
                               drop_suspended=drop_suspended,
                               fields=fetch_fields
                               )
    if len(df) == 0:
        columns = fields
        for label in columns:
            if label in prev_close_based_dynamic_fields:
                df[label] = 0  # 动态字段,简单复制一下列名
        df = df[fields]
    else:
        if dynamic_filed:  # 如果有动态字段，则需要昨日价格
            df = _calc_prev_close(df)

            if start_date is not None: # 如果指定了开始日期，则为了取前一日数据有可能存在超出日期范围的数据
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df = df.truncate(before=start_date, after=end_date, copy=False)

        if adjust_type == 'pre':  # 前复权
            # 除权处理
            # 利用收盘价计算最后一天的复权系数

            # 因为复权会修改数据，因此需要复制数据
            df_copy = df[['factor']].copy()  # 做一个新的 DataFrame 出来并且保留Index

            if multiple_codes:
                factor = get_relevant_factor(df[['code', 'factor']])
            else:
                factor = get_relevant_factor(df['factor'])

            columns = fields
            for label in columns:
                # 保留两位小数，需不需要四舍五入？
                if label in ['open', 'high', 'low', 'close']:
                    # 利用复权系数调整所有价格相关数据
                    df_copy[label] = (df[label] / factor).map('{:.2f}'.format).astype(float)  # 除权
                else:
                    if label in prev_close_based_dynamic_fields:  # 动态字段
                        df_prev_close = (df['prev_close'] / factor).map('{:.2f}'.format).astype(float)

                        if 'prev_close' == label:  # 涨幅
                            df_copy[label] = df_prev_close
                        elif 'pt_close' == label:  # 涨幅
                            df_close = (df['close'] / factor).map('{:.2f}'.format).astype(float)
                            df_copy[label] = ((df_close / df_prev_close) * 100 - 100) \
                                .map('{:.2f}'.format).astype(float)
                            del df_close
                        elif 'pt_ampl' == label:  # 震幅
                            df_high = (df['high'] / factor).map('{:.2f}'.format).astype(float)
                            df_low = (df['low'] / factor).map('{:.2f}'.format).astype(float)
                            df_copy[label] = (((df_high - df_low) / df_prev_close) * 100) \
                                .map('{:.2f}'.format).astype(float)
                            del df_high
                            del df_low
                        del df_prev_close
                    else:
                        df_copy[label] = df[label]  # 其他字段直接复制

            df = df_copy.drop('factor', axis=1)  # 对外隐藏 factor 列
            del df_copy
            del factor
        else:  # 不复权
            # 为了防止外面修改原始DataFrame数据，统一复制一次?
            # df = df.copy()
            if dynamic_filed:
                # FIXME 需要处理动态字段
                pass
            raise NotImplemented('非前复权未实现')

    # 字段名称兼容转换（字段改名）
    if filed_name_changed and isinstance(df, pd.DataFrame):
        df.rename(columns=dict(zip(fields, original_fields)), inplace=True)

    if not multiple_codes:  # 传入一个code
        if single_fields:
            # 一个field，取出一列数据，格式为 Pandas Series
            df = df.iloc[:, 0]

        if single_date:
            # 单日date，取出一行数据，如果已经是 Series 则取出一个数据
            df = df.iloc[0] if len(df) > 0 else None
    else:  # 传入多个code
        if single_date:
            # 单日date，去掉日期列，把 code 列变成 index
            df.set_index('code', inplace=True)

            if single_fields:
                # 一个field，取出一列数据，格式为 Pandas Series
                df = df.iloc[:, 0] if len(df) > 0 else None

    # 可以根据现有数据动态计算出来的字段
    # prev_close
    # pt_close
    # pt_ampl,
    #
    # money_major,pt_money_major,
    # pt_money_huge,
    # pt_money_large,
    # pt_money_medium,
    # pt_money_small
    #
    # ma5

    return df


def get_day_heat(code_or_codes, date=None, backs=0):
    """
    获得股票活跃度
    :param code_or_codes:
    :param date:
    :param backs:
    :return:
    """

    # 活跃度先简单的以涨跌幅为活跃度
    df = get_day(code_or_codes, date=date, backs=backs, fields='pt_close')

    if df is not None:
        if isinstance(df, pd.Series):
            df.rename('heat', inplace=True)
        elif isinstance(df, pd.DataFrame):
            df.rename(columns=lambda x: 'heat' if x == 'pt_close' else x, inplace=True)

    return df
