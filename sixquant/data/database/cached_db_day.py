# coding=utf-8

import datetime
from ...option import option
from ...utils.exceptions import IllegalArgumentError
from ...utils.datetime_utils import get_delta_trade_day
from .db import db


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

    def get_day(self, code_or_codes, start_date, end_date, backs, fields):
        """
        得到股票日线数据

        Parameters
        ----------
        code_or_codes : str/str array
            单个股票代码或股票代码数组
        start_date : date str/date
            数据开始日期
            start_date 和 backs 同时出现时忽略 start_date 参数
        end_date : date str/date
            数据结束日期
            和 backs 参数配套使用时表示取某一天以及前 backs 个数据
        backs : int
            保证所有数据从结束日期往前有 n 条记录，以便用来画图等
            start_date 和 backs 同时出现时忽略 start_date 参数
        fields : str/str array
            单个字段名称或字段名称数组

        Notes
        -----
        请尽可能的用的时候取数据，而不是一次性取

        Returns
        -------
        Pandas DataFrame
        """
        if start_date is None and backs < 1:
            raise IllegalArgumentError('either start_date or backs must be defined!')

        if end_date is None:
            raise IllegalArgumentError('end_date is None!')

        if backs > 0 and start_date is None:
            start_date = get_delta_trade_day(end_date, -backs)  # 一般情况下(不包括停牌的数据)直接往前取 backs 个交易日的数据

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

            if backs > 0:
                # 检查数据是否满足要求
                print(df)
                import pandas as pd
                d = pd.DataFrame()
                #print(d.groupby('code').count())

        return df


cached_db_day = CachedDatabaseDay()
