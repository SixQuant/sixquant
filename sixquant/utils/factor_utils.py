# coding=utf-8

import pandas as pd

"""复权因子辅助函数"""


def get_relevant_factor(df):
    """
    计算相应的复权因子数据
    :return:
    返回单个复权因子或复权因子数组numpy.ndarray
    """
    if isinstance(df, pd.Series):
        # 单个股票只需要返回一个因子数据，所有行都会除以这个数字
        factor = df.loc[df.index.max()]
    else:
        # 多个股票需要按照股票代码填充出长度与数据行数一样多的因子 Series

        # 1. 获得每个股票的最后一天复权因子
        df.index.name = 'date'
        df = df.reset_index()
        factor_max = df.loc[df.groupby(['code'])['date'].idxmax()][['code','factor']].values

        # 2. 用上面获得的复权因子填充到所有日期
        for code, value in factor_max:
            df.loc[df.code == code, 'factor'] = value

        del factor_max
        factor = df['factor'].values
    return factor
