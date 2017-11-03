# coding=utf-8

import os
import click
import requests

import numpy as np
import pandas as pd

from .logger import logger
from .constants import BUNDLE_SERVER_URL
from .option import option
from .fmt import fmt_file_size
from .utils import to_date_object, to_date_str
from .utils import get_last_trading_day, get_last_histrade_day, get_next_trade_day
from .RecycleTimer import RecycleTimer
from .db import db


class DailyUpdater(object):
    """"
    每日数据更新下载
    """

    def __init__(self, verbose=False):
        super().__init__()
        self.verbose = verbose

    def update(self, start_date=None):
        if start_date is None:
            date = get_last_histrade_day(-30 + 1)  # 默认同步前30个工交易日数据
        else:
            date = to_date_object(start_date, date_only=True)

        date_end = get_last_trading_day()

        log = logger.get(__name__)
        dt_range = to_date_str(date) if date == date_end else (to_date_str(date) + ' ~ ' + to_date_str(date_end))
        log.debug('updating stock bundle(' + dt_range + ')')

        while date <= date_end:
            self.update_bundle(date)
            date = get_next_trade_day(date)

    def update_bundle(self, date):
        log = logger.get(__name__)

        key = 'bundle-' + to_date_str(date) + '.gzip'

        # 文件是否已经在远程存在
        target = BUNDLE_SERVER_URL + key
        r = requests.head(target)
        if 200 != r.status_code:
            log.warning('remote server missing stock bundle ' + target)
            return False

        total_length = int(r.headers.get('Content-Length'))
        last_modified = to_date_object(r.headers.get('Last-Modified'))

        local_file = option.get_data_filename('bundle', key)
        if os.path.exists(local_file):
            local_modified = os.path.getmtime(local_file)
            if local_modified == last_modified.timestamp():
                return False  # 本地文件最后修改时间和远程一致

        log.debug('downloading stock bundle data on ' + to_date_str(date) +
                  ', file size ' + fmt_file_size(total_length))

        path = option.get_data_filename('bundle')
        if not os.path.exists(path):
            os.makedirs(path)

        r = requests.get(target, stream=True)
        if r.status_code != 200:
            return False

        out = open(local_file, 'wb')
        if total_length <= 8192 * 1024:
            for data in r.iter_content(chunk_size=8192):
                out.write(data)
        else:
            with click.progressbar(length=total_length, label="downloading ...") as bar:
                for data in r.iter_content(chunk_size=8192):
                    bar.update(len(data))
                    out.write(data)
        out.close()

        # 修正文件创建时间
        os.utime(local_file, (last_modified.timestamp(), last_modified.timestamp()))

        # 导入到本地数据库
        df = pd.read_csv(local_file, dtype={1: np.str}, compression='gzip')
        df.set_index(df.columns[0], inplace=True)
        df.index.name = None
        df.index = pd.to_datetime(df.index)
        db.put_day(df)

        return True

    def start(self, start_date):
        """启动一个独立线程循环抓取数据"""
        timer = RecycleTimer(interval=60,  # 最小间隔时间(s)
                             callback=self.update,
                             async=True,
                             daemon=True,
                             async_thread_name='Daily-Updater')
        timer.start()


daily_updater = DailyUpdater()
