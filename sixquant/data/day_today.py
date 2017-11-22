# coding=utf-8

import numpy as np
import pandas as pd

from ..constants import TODAY_QUOTE_FILE, TODAY_MONEY_FILE, TODAY_FILE, TODAY_SMALL_FILE, \
    TODAY_SMALL_NO_ST_NO_SUBNEW_FILE
from ..utils.dataframe_utils import request_dataframe
from .basic import get_stocks


def _request_day_today(url, fields=None, dropna=True):
    df = request_dataframe(url, dtype={0: np.str})
    if df is not None:
        if dropna:
            df.dropna(inplace=True)

        df.set_index(df.columns[0], inplace=True)
        df.index.name = None
        df['time'] = pd.to_datetime(df['time'])

        if fields is not None:
            df = df[fields]
    return df


def get_day_today_quote(fields=None, dropna=True):
    """
    得到今日个股实时股价数据（包括停牌的股）
    :param fields:
    :param dropna: 是否删除空行（即是否包括停牌的股）
    :return: DataFrame
    """
    return _request_day_today(TODAY_QUOTE_FILE, fields=fields, dropna=dropna)


def get_day_today_money(fields=None, dropna=True):
    """
    得到今日个股实时资金数据（包括停牌的股）
    :param fields:
    :param dropna: 是否删除空行（即是否包括停牌的股）
    :return: DataFrame
    """
    return _request_day_today(TODAY_MONEY_FILE, fields=fields, dropna=dropna)


def get_day_today(fields=None,
                  dropna=True,
                  small_only=False,
                  st_only=False,
                  subnew_only=False,
                  no_st=False,
                  no_subnew=False):
    """
    得到今日个股实时股价数据（包括停牌的股）
    :param fields:
    :param dropna: 是否删除空行（即是否包括停牌的股）
    :param small_only: 是否只要小市值股
    :param st_only: 是否只要 ST 股
    :param subnew_only: 是否只要次新股（一年以内的股票称为次新股）
    :param no_st: 是否包含 ST 股
    :param no_subnew: 是否包含次新股（一年以内的股票称为次新股）
    :return: DataFrame
    """
    if small_only and not st_only and not subnew_only and no_st and no_subnew:
        return _request_day_today(TODAY_SMALL_NO_ST_NO_SUBNEW_FILE, fields=fields, dropna=dropna)
    if small_only and not st_only and not subnew_only and not no_st and not no_subnew:
        return _request_day_today(TODAY_SMALL_FILE, fields=fields, dropna=dropna)
    else:
        df = _request_day_today(TODAY_FILE, fields=fields, dropna=dropna)
        if small_only or st_only or subnew_only or no_st or no_subnew:
            stocks = get_stocks(small_only=small_only,
                                st_only=st_only,
                                subnew_only=subnew_only,
                                no_st=no_st,
                                no_subnew=no_subnew)
            df = df.loc[stocks]
        return df


def get_day_today_small(fields=None, dropna=True):
    """
    得到今日个股实时股价数据（小盘股，包括停牌的股）
    :param fields:
    :param dropna: 是否删除空行（即是否包括停牌的股）
    :return: DataFrame
    """
    return get_day_today(fields=fields, dropna=dropna, small_only=True)


def get_day_today_small_no_st_no_subnew(fields=None, dropna=True):
    """
    得到今日个股实时股价数据（小盘股不要ST不要次新，包括停牌的股）
    :param fields:
    :param dropna: 是否删除空行（即是否包括停牌的股）
    :return: DataFrame
    """
    return get_day_today(fields=fields, dropna=dropna, small_only=True, no_st=True, no_subnew=True)
