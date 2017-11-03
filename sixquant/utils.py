# coding=utf-8

import time
import datetime
from functools import lru_cache
from io import StringIO

import numpy as np
import pandas as pd

from .constants import HOLYDAYS_FILE
from .option import option
from .Fetcher import fetcher
from .DailyCache import daily_cache
from .DailyFuncCacheWatcher import daily_func_cache_watcher


def request_dataframe(url, dtype=None):
    """
    从网络中加载 DataFrame，支持压缩等，比原装的性能要好
    :param url:
    :param dtype:
    :return:
    """
    status, data = fetcher.http_get_text(url)
    if status == 200:
        return pd.read_csv(StringIO(data), dtype=dtype)
    return None


def to_date_str_fmt(date, fmt):
    """
    转换为日期字符串
    :param date:
    :param fmt:
    :return:
    """
    if date is None:
        return ""

    date = to_date_object(date)
    return date.strftime(fmt)


def to_date_str(date):
    """转换为日期字符串 %Y-%m-%d
    :param date:
    :return:
    """
    return to_date_str_fmt(date, '%Y-%m-%d')


def to_date_str_short(date):
    """转换为日期字符串 %Y-%m-%d
    :param date:
    :return:
    """
    return to_date_str_fmt(date, '%Y%m%d')


def to_date_object(date, date_only=False):
    """
    转换对象为日期对象
    :param date:
    :param date_only: 是否只保留日期部分
    :return:
    """
    if date is None:
        return None

    inc_time_part = False
    adjust_time_zone = False

    if isinstance(date, str):
        n = len(date)
        if 8 == n:
            fmt = '%Y%m%d'
        elif 10 == n:
            pos = date.find('/')
            if -1 == pos:
                fmt = '%Y-%m-%d' if 4 == date.find('-') else '%m-%d-%Y'
            elif 4 == pos:
                fmt = '%Y/%m/%d'
            else:
                fmt = '%m/%d/%Y'
        elif n > 4 and date[n - 4:] == ' GMT':
            fmt = '%a, %d %b %Y %H:%M:%S GMT'
            adjust_time_zone = True  # 需要调整时区
            inc_time_part = True
        else:
            fmt = '%Y-%m-%d %H:%M:%S'
            inc_time_part = True
        date = datetime.datetime.strptime(date, fmt)

        # 需要调整时区
        if adjust_time_zone:
            date = date + datetime.timedelta(seconds=-time.timezone)

    if isinstance(date, np.datetime64):
        date = datetime.datetime.fromtimestamp(date.astype('O') / 1e9)
        inc_time_part = True

    if not isinstance(date, datetime.date):
        raise TypeError('date type error!' + str(date))

    if date_only:
        date = date.date()

    return date


def is_holiday(date):
    """
    判断是否节假日
    """
    key = 'holidays'
    holidays = daily_cache.get(key)
    if holidays is None:
        status, data = fetcher.http_get_text(HOLYDAYS_FILE)
        if status == 200:
            holidays = set()
            for line in data.split('\n'):
                n = len(line)
                if n > 0 and line[n - 1] == '\n':
                    line = line[:n - 1]
                    n -= 1
                if n == 8:
                    holidays.add(int(line))
            daily_cache.set(key, holidays)

    date = to_date_object(date)
    date = date.year * 10000 + date.month * 100 + date.day
    return date in holidays


def is_same_day(d1, d2):
    """
    判断两个日期是同一天，忽略时分秒
    :param d1:
    :param d2:
    :return: bool
    """
    d1 = to_date_object(d1)
    d2 = to_date_object(d2)
    return d1.year == d2.year and d1.month == d2.month and d1.day == d2.day


def is_same_or_later_day(d1, d2):
    """
    判断d2是否等于或晚于d1，忽略时分秒
    :param d1:
    :param d2:
    :return: bool
    """
    d1 = to_date_object(d1)
    d2 = to_date_object(d2)
    d1 = d1.year * 10000 + d1.month * 100 + d1.day
    d2 = d2.year * 10000 + d2.month * 100 + d2.day

    return d2 >= d1


def month_delta(date, months):
    """
    增减月数
    :param date:
    :param months:
    :return:
    """
    date = to_date_object(date)

    y = date.year
    if months >= 0:
        y = y + int((date.month + months - 1) / 12)
        m = int((date.month + months) % 12)
        if 0 == m:
            m = 12
    else:
        y = y + int((date.month + months - 12) / 12)
        m = int((date.month + months) % 12)
        if 0 == m:
            m = 12

    date = datetime.datetime(y, m, date.day)
    return date


def is_holiday_today():
    """
    判断今天是否是节假日
    :return: bool
    """
    today = datetime.date.today().strftime('%Y%m%d')
    return is_holiday(today)


@lru_cache(1024)  # 缓存耗时的函数调用
def is_trading_day(date):
    """
    判断是否为交易日
    :param date:
    :return: bool
    """
    date = to_date_object(date)
    weekday = date.weekday() + 1
    if weekday >= 6:
        return False

    return not is_holiday(date)


def is_trading_day_today():
    """
    判断今天是否是交易日
    :return: bool
    """
    return is_trading_day(datetime.date.today())


def is_trading_time():
    """
    判断现在是否为交易时间以便非交易时间不需要抓取实时数据
    @:param delay 延迟多少秒
    """

    if option.debugging:
        return True

    if not is_trading_day_today():
        return False

    hour = time.hour
    minute = time.minute

    if hour == 9:  # 上午开盘
        return True
    if hour == 10:
        return True
    if hour == 11 and minute <= 35:  # 上午收盘多加 5 分钟
        return True
    if hour == 13:  # 下午开盘
        return True
    if hour == 14:
        return True
    if hour == 15 and minute <= 5:  # 下午收盘多加 5 分钟
        return True

    return False


def get_last_trading_day():
    """
    返回最近一个交易日
    :return: date
    """
    date = datetime.date.today()
    if datetime.datetime.now().hour <= 8:
        date = date + datetime.timedelta(days=-1)  # 8点前要往前一天

    while not is_trading_day(date):
        date = date + datetime.timedelta(days=-1)
    return date


@lru_cache(128)
def get_last_histrade_day(days=0):
    """
    返回最近一个历史交易日
    :return:
    """

    daily_func_cache_watcher.watch_lru_cache(get_last_histrade_day)

    last_trading_day = get_last_trading_day()  # 最近的一个交易日
    if is_same_day(datetime.date.today(), last_trading_day):
        if datetime.datetime.now().hour <= 16:
            # 最后一个交易日时间，并且现在是16点前要往前一天，因为今天还不可能有数据
            days -= 1

    if days < 0:  # 往前多少个交易日
        delta = 0
        while delta != days:
            last_trading_day = last_trading_day + datetime.timedelta(days=-1)
            if is_trading_day(last_trading_day):
                delta -= 1

    return last_trading_day


def get_delta_trade_day(date, days):
    """
    返回前后days个交易日
    :return:
    """
    trade_day = to_date_object(date)
    step = -1 if days < 0 else +1

    delta = 0
    while delta != days:
        trade_day = trade_day + datetime.timedelta(days=step)
        if is_trading_day(trade_day):
            delta += step

    return trade_day


def get_prev_trade_day(date):
    """获取上一交易日"""
    return get_delta_trade_day(date, -1)


def get_next_trade_day(date):
    """获取下一交易日"""
    return get_delta_trade_day(date, +1)
