# coding=utf-8

import pandas as pd

from ..utils.datetime_utils import get_delta_trade_day, get_last_histrade_day, to_date_object
from .basic import translate_stock_code
from .database.cached_db_day import cached_db_day

"""
股票日线信息
"""


def get_day(code_or_codes,
            start_date=None,
            end_date=None,
            fields=None,
            adjust_type='pre'
            ):
    """
    得到股票日线数据

    传入一个code，一个field，函数会返回 Pandas Series
    传入一个code，多个field，函数会返回 Pandas DataFrame
    传入多个code，一个field，函数会返回 Pandas DataFrame
    传入多个code，多个field，函数会返回 Pandas MultiIndex DataFrame
                                    df.loc['300315'].loc['2017-10-08':'2017-10-09']

    :param code_or_codes:
    :param start_date:
    :param end_date:
    :param fields:
    :param adjust_type:
    :return:
    """
    # TODO: 应该为单只股票某个时间段数据特别优化？
    multiple_codes = not isinstance(code_or_codes, str)  # 是否同时取多个股票数据

    if start_date is None:
        start_date = get_last_histrade_day(-10)  # 默认取最近的前10个交易日

    if fields is None:
        fields = ['open', 'high', 'low', 'close', 'volume', 'amount']  # 全部字段
    elif isinstance(fields, str):
        fields = [fields]

    fetch_fields = ['code']  # 需要额外的字段

    if adjust_type == 'pre':
        fetch_fields.append('factor')  # 需要额外的字段用于计算

    for x in fields:  # 合并上用户真正想要的字段
        if x not in fetch_fields:
            fetch_fields.append(x)

    # 获取原始数据 Pandas MultiIndex DataFrame(code,date)
    code_or_codes = translate_stock_code(code_or_codes)
    df = cached_db_day.get_day(code_or_codes=code_or_codes, start_date=start_date, end_date=end_date,
                               fields=fetch_fields)

    if len(df) > 0:
        if adjust_type == 'pre':  # 前复权
            # 除权处理
            # 利用收盘价计算最后一天的复权系数
            factor = df.loc[df.index.max()]['factor']

            # 因为复权会修改数据，因此需要复制数据
            df_copy = df[['factor']].copy()  # 做一个新的 DataFrame 出来并且保留Index

            if multiple_codes:
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
        else:  # 不复权
            # 为了防止外面修改原始DataFrame数据，统一复制一次?
            # df = df.copy()
            pass

    if not multiple_codes and len(fields) == 1:
        # 传入一个code，一个field，函数会返回 Pandas Series
        df = df.iloc[:, 0]

    # 可以根据现有数据动态计算出来的字段
    # pt_price
    # pt_ampl,
    #
    # money_major,pt_money_major,
    # pt_money_huge,
    # pt_money_large,
    # pt_money_medium,
    # pt_money_small
    #
    #  ma5

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
