# coding=utf-8

import datetime
import re


def fmt_round_number(count, keep_width=False):
    """
    Round a floating point number to two decimal places in a human friendly format.
    :param count: The number to format.
    :param keep_width: :data:`True` if trailing zeros should not be stripped,
                       :data:`False` if they can be stripped.
    :returns: The formatted number as a string. If no decimal places are
              required to represent the number, they will be omitted.
    The main purpose of this function is to be used by functions like
    :func:`format_length()`, :func:`format_size()` and
    :func:`format_timespan()`.
    Here are some examples:
    >>> fmt_round_number(1)
    '1'
    >>> fmt_round_number(math.pi)
    '3.14'
    >>> fmt_round_number(5.001)
    '5'
    """
    text = '%.2f' % float(count)
    if not keep_width:
        text = re.sub('0+$', '', text)
        text = re.sub('\.$', '', text)
    return text


def fmt_file_size(size):
    """
    返回可读性较好的文件大小字符串
    :param size:
    :return:
    """
    if size < 1024:
        return str(size)
    if size < 1024 * 1024:
        return fmt_round_number(size / float(1024)) + 'K'
    if size < 1024 * 1024 * 1024:
        return fmt_round_number(size / float(1024 * 1024)) + 'M'
    if size < 1024 * 1024 * 1024 * 1024:
        return fmt_round_number(size / float(1024 * 1024 * 1024)) + 'G'
    if size < 1024 * 1024 * 1024 * 1024 * 1024:
        return fmt_round_number(size / float(1024 * 1024 * 1024 * 1024)) + 'T'

    return fmt_round_number(size / float(1024 * 1024 * 1024 * 1024 * 1024)) + 'P'


def fmt_money(money):
    """
    返回可读性较好的钱数字符串
    :param money:
    :return:
    """
    if money is None:
        return ''

    x = money if money >= 0 else -money

    if x >= 10000 * 10000:
        return fmt_round_number(money / (10000 * 10000)) + '亿'

    if x >= 1000 * 10000:
        return fmt_round_number(money / (1000 * 10000)) + '千万'

    if x >= 100 * 10000:
        return fmt_round_number(money / (100 * 10000)) + '百万'

    if x >= 10000:
        return fmt_round_number(money / 10000) + '万'
    return str(money)


def fmt_numpy_datetime64(t, fmt):
    """
    转换并格式化numpy的日期对象
    :param t:
    :param fmt:
    :return:
    """
    if t is None:
        return ''

    return datetime.datetime.fromtimestamp(t.astype('O') / 1e9).strftime(fmt)
