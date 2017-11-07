# coding=utf-8
import datetime

import pandas as pd

from sixquant import option
from .db import db
from ...utils.datetime_utils import to_date_object


class CachedDatabaseDay(object):
    """
    数据库支持（SQLite3）
    """

    def __init__(self):
        self.cached_df = None

        self.start_date = None
        self.end_date = None
        self.fields = None

    def _lock_acquire(self):
        pass

    def _lock_release(self):
        pass

    def reset(self):
        self.cached_df = None

        self.start_date = None
        self.end_date = None
        self.fields = None

    def _prepare(self, start_date, end_date, fields):
        """
        缓存所有股票数据
        :param start_date:
        :param end_date:
        :param fields:
        :return:
        """
        self._lock_acquire()
        try:
            reload = False
            if self.cached_df is None:
                reload = True
                self.start_date = start_date
                self.end_date = end_date

                self.fields = ['code', 'factor']
                for x in fields:
                    if x not in self.fields:
                        reload = True
                        self.fields.append(x)
            else:
                if start_date < self.start_date:
                    reload = True
                    self.start_date = start_date

                if end_date > self.end_date:
                    reload = True
                    self.end_date = end_date

                for x in fields:
                    if x not in self.fields:
                        reload = True
                        self.fields.append(x)

            if reload:
                self.cached_df = db.get_day_all(start_date=start_date, end_date=end_date, fields=self.fields)

            df = self.cached_df

            if not option.enable_caching_day:
                self.reset()

            return df

        finally:
            self._lock_release()

    def get_day(self, code_or_codes, start_date, end_date, fields):
        """
        检索日线数据
        :param code_or_codes:
        :param start_date:
        :param end_date:
        :param fields:
        :return:
        """

        start_date = to_date_object(start_date, date_only=True)
        if start_date is None:
            raise ValueError('start_date is None!')

        if end_date is None:
            end_date = datetime.date.today()
        else:
            end_date = to_date_object(end_date, date_only=True)

        # 获取数据，已经按照日期排序
        df = self._prepare(start_date=start_date, end_date=end_date, fields=fields)
        if df is not None and len(df) > 0:
            # 先用索引做日期条件过滤
            if start_date is not None and end_date is not None:
                df = df.truncate(before=start_date, after=end_date)
                # df = df.loc[(df.index >= pd.to_datetime(start_date)) &
                #            (df.index <= pd.to_datetime(end_date))]
            elif start_date is not None:
                df = df.truncate(before=start_date)
                # df = df.loc[df.index >= pd.to_datetime(start_date)]
            elif end_date is not None:
                df = df.truncate(after=end_date)
                # df = df.loc[df.index <= pd.to_datetime(end_date)]

            # 然后在这基础上再做其他条件过滤
            if code_or_codes is not None:
                if isinstance(code_or_codes, str):
                    df = df.loc[df.code == code_or_codes]
                else:
                    df = df.loc[df.code.isin(code_or_codes)]

        return df


cached_db_day = CachedDatabaseDay()
