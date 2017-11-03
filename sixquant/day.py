# coding=utf-8

import os
import pandas as pd

from .DailyCache import daily_cache
from .utils import get_delta_trade_day, get_last_histrade_day, to_date_object
from .option import option
from .basic import get_stock_code

"""
股票日线信息
"""


def get_day(stocks, start_date=None, end_date=None, fields=None, adjust_type='pre'):
    """
    得到股票日线数据
    :param stocks:
    :param start_date:
    :param end_date:
    :param fields:
    :param adjust_type:
    :return:
    """

    if not isinstance(stocks, str):
        rs = []
        for stock in stocks:
            _df = get_day(stock, start_date=start_date, end_date=end_date, fields=fields, adjust_type=adjust_type)
            if _df is not None and len(_df) > 0:
                _df['code'] = stock
                rs.append(_df)
        _df = pd.concat(rs)
        cols = _df.columns.tolist()
        cols = [cols[-1]] + cols[:-1]
        _df = _df.reindex(columns=cols)
        return _df

    stock = get_stock_code(stocks)

    key = stock + '-day'
    _df = daily_cache.get(key)
    if _df is None:
        filename = option.get_data_filename('day', stock + '.csv' + '.gzip')
        if not os.path.exists(filename):
            return None

        _df = pd.read_csv(filename, compression='gzip')
        _df.set_index(_df.columns[0], inplace=True)
        _df.index.name = None
        _df.index = pd.to_datetime(_df.index)
        daily_cache.set(key, _df)  # 缓存全部数据

    if start_date is None:
        start_date = get_last_histrade_day(-10 + 1)  # 最近的前10个交易日

    _df = _df.loc[_df.index >= pd.to_datetime(to_date_object(start_date))]

    if end_date is not None:
        _df = _df.loc[_df.index <= pd.to_datetime(to_date_object(end_date))]

    if len(_df) > 0:
        # 除权处理
        factor = 1
        if adjust_type is None:  # 不复权
            factor = 1
        elif adjust_type == 'pre':  # 前复权
            # 利用收盘价计算复权系数
            factor = _df.loc[_df.index.max()]['factor']  # 后面将用最后一天的复权系数进行数据调整

        # 利用最后一天的复权系数调整所有价格相关数据
        # 因为复权会修改数据，因此需要复制
        if fields is not None:
            columns = fields
        else:
            columns = _df.columns.tolist()
            columns.remove('factor')

        _df_copy = _df[['factor']].copy()  # 做一个新的 DataFrame 出来并且保留Index
        for label in columns:
            if label in ['open', 'high', 'low', 'close']:
                if adjust_type is None:
                    _df_copy[label] = _df[label] / _df['factor']  # 不复权
                elif adjust_type == 'pre':
                    _df_copy[label] = _df[label] / factor  # 前复权

                    # 保留两位小数，需不需要四舍五入？
                    _df_copy[label] = _df_copy[label].map('{:.2f}'.format).astype(float)
            else:
                _df_copy[label] = _df[label]  # 其他字段直接复制
        _df = _df_copy.drop('factor', axis=1)  # 对外隐藏 factor 列

    return _df


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

    stock = get_stock_code(stocks)

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
