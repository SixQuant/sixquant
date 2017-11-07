# coding=utf-8

from io import StringIO
import pandas as pd
from .fetcher import fetcher


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
