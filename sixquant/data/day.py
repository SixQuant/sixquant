# coding=utf-8

import pandas as pd

from ..utils.exceptions import IllegalArgumentError
from ..utils.ds_utils import append_if_not_exists
from ..utils.field_name_translator import translate_field_name
from ..utils.datetime_utils import get_delta_trade_day, get_last_histrade_day, to_date_object
from .basic import translate_stock_code
from .database.cached_db_day import cached_db_day

"""
股票日线信息
"""


def get_day(code_or_codes,
            start_date=None,
            end_date=None,
            date=None,
            backs=0,
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
        start_date 和 backs 同时出现时忽略 start_date 参数
    end_date : date str/date
        数据结束日期
    date : date str/date
        等价于 end_date
        一般表示只取某一天的数据
        和 backs 参数配套使用时表示取某一天以及前 backs 个数据
    backs : int
        保证所有数据从结束日期往前有 n 条记录，以便用来画图等
        start_date 和 backs 同时出现时忽略 start_date 参数
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

    # 缺省参数处理
    if end_date is None:
        end_date = get_last_histrade_day(0)  # 默认取最后一个交易日
    else:
        end_date = to_date_object(end_date, date_only=True)

    if backs > 0:  # start_date 和 backs 同时出现时忽略 start_date 参数
        start_date = None
    else:
        if start_date is None:
            start_date = end_date  # 默认取1个交易日
        else:
            start_date = to_date_object(start_date, date_only=True)

    if fields is None:
        fields = ['open', 'high', 'low', 'close', 'volume', 'amount']  # 全部字段
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

    if 'pt_close' in fields:
        backs = 1 if backs < 1 else backs  # 需要前一天的数据

    # 获取原始数据 Pandas MultiIndex DataFrame(code,date)
    code_or_codes = translate_stock_code(code_or_codes)
    df = cached_db_day.get_day(code_or_codes=code_or_codes,
                               start_date=start_date,
                               end_date=end_date,
                               fields=fetch_fields,
                               backs=backs)

    if len(df) > 0:
        if adjust_type == 'pre':  # 前复权
            # 除权处理
            # 利用收盘价计算最后一天的复权系数
            factor = df.loc[df.index.max()]['factor']

            # 因为复权会修改数据，因此需要复制数据
            df_copy = df[['factor']].copy()  # 做一个新的 DataFrame 出来并且保留Index

            if multiple_codes and isinstance(factor, pd.Series):
                # 同时处理多只股票数据，需要制作并使用 factor 因子 DataFrame
                step = len(factor)
                step_max = len(df_copy) - step
                step_i = 0
                while step_i < step_max:
                    df_copy.iloc[step_i:step_i + step, 0] = factor.values
                    step_i += step

                factor = df_copy['factor']

            columns = fields
            for label in columns:
                if label in ['open', 'high', 'low', 'close']:
                    # 利用复权系数调整所有价格相关数据
                    # print(df[label])
                    # print(factor)
                    # print(df[label] / factor)
                    df_copy[label] = df[label] / factor  # 除权

                    # 保留两位小数，需不需要四舍五入？
                    df_copy[label] = df_copy[label].map('{:.2f}'.format).astype(float)
                else:
                    df_copy[label] = df[label]  # 其他字段直接复制
            df = df_copy.drop('factor', axis=1)  # 对外隐藏 factor 列
            del df_copy
            del factor
        else:  # 不复权
            # 为了防止外面修改原始DataFrame数据，统一复制一次?
            # df = df.copy()
            pass

    # 字段名称兼容转换
    if filed_name_changed and isinstance(df, pd.DataFrame):
        df.rename(columns=dict(zip(fields, original_fields)), inplace=True)

    if not multiple_codes:  # 传入一个code
        if single_fields:
            # 一个field，取出一列数据，格式为 Pandas Series
            df = df.iloc[:, 0]

        if single_date:
            # 单日date，取出一行数据，如果已经是 Series 则取出一个数据
            df = df.iloc[0]
    else:  # 传入多个code
        if single_date:
            # 单日date，去掉日期列，把 code 列变成 index
            df.set_index('code', inplace=True)

            if single_fields:
                # 一个field，取出一列数据，格式为 Pandas Series
                df = df.iloc[:, 0]

    # 可以根据现有数据动态计算出来的字段
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


def get_day_amount(stocks, start_date=None, end_date=None):
    """返回每日成交额
    :param stocks:
    :param start_date:
    :param end_date:
    :return:
    """
    df = get_day(stocks, start_date=start_date, end_date=end_date, fields=['amount'])
    return df


def get_day_heat(stocks, start_date, end_date):
    """
    获得股票活跃度
    :param stocks:
    :param start_date:
    :param end_date:
    :return:
    """
    if not isinstance(stocks, str):
        rs = []
        for stock in stocks:
            df = get_day_heat(stock, start_date=start_date, end_date=end_date)
            if df is not None and len(df) > 0:
                df['code'] = stock
                rs.append(df)
        df = pd.concat(rs)
        cols = df.columns.tolist()
        cols = [cols[-1]] + cols[:-1]
        df = df.reindex(columns=cols)
        return df

    stock = translate_stock_code(stocks)

    df = get_day(stock,
                 start_date=get_delta_trade_day(start_date, -1),
                 end_date=end_date,
                 fields=['close'])

    if df is not None and len(df) > 0:
        # 计算活跃度
        df['heat'] = df.shift(1)['close']  # 前一天收盘价
        df['heat'] = ((df['close'] - df['heat']) * 100 / df['heat']).round(2)  # 求涨幅
        # 先简单的以涨跌幅为活跃度
        # df['heat'] = df['heat'] + 10 # 跌 10% 为0 涨10变为20
        # df[df.heat>20] = 10
        # df[df.heat<0]  = 0

        df = df[['heat']]
        df = df.drop(df.index[0])  # 删除第一行空行

    return df


def calc_day_pt_of_change(df):
    """
    将 DataFrame 中的价格部分['open', 'high', 'low', 'close']转换为涨幅
    :param df: 需要多一行昨日的数据
    :return: 应为其中有一行数据是昨日收盘价，因此最终结果会少一行数据
    """
    df = df.copy()  # 因为后面会修改数据，所以复制一个 DataFrame
    df = df.sort_index(ascending=True)  # 为了保险起见，对日期进行一次排序
    df_pre_close = df['close'].shift(1)  # 前一天的收盘价

    for label in df.columns.tolist():
        if label in ['open', 'high', 'low', 'close']:
            df[label] = ((df[label] - df_pre_close) * 100 / df_pre_close).round(2)  # 价格部分变成涨幅
        else:
            df[label] = df[label]  # 其他字段直接复制
    df = df.drop(df.index[0])  # 删除第一行空行
    return df
