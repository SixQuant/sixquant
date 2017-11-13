# coding=utf-8

import pandas as pd
from ...option import option
from ...utils.logger import logger
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
        log = logger.get(__name__)
        log.debug('reset daily data cache.')

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

    def _get_backs_from_cache(self, code, date, backs, fields):
        """
        从缓存中获取 date 日往前 backs 个数据，同时检查 date 日是否有数据
        :param code:
        :param date:
        :param backs:
        :param fields:
        :return: (df, exists, full)
            exists: True/False, 表示 date 日是否有数据
            full: True/False, 表示 date 日是否有数据
        """
        self._lock_acquire()
        try:
            df = self.cached_df
            df = df.loc[df.code == code]  # 先按照股票代码过滤剩下该股票的所有数据
            try:
                i = df.index.get_indexer_for(df.loc[df.index == date].index)[0]  # 得到 date 这一天的行号
            except IndexError:
                return None, False, False  # 这一天没有数据

            if i == -1 or i < backs:
                return None, True, False  # 数据不够直接返回 None

            df = df.iloc[i - backs:i + 1][fields]

            return df, True, df is not None and len(df) == backs + 1

        finally:
            self._lock_release()

    def get_day(self, code_or_codes, start_date, end_date, backs, drop_suspended, fields):
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
        drop_suspended : bool
            是否直接丢弃中间有停牌的数据
            和 backs 配套使用
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
                start_date = pd.to_datetime(start_date)
                end_date = pd.to_datetime(end_date)
                df = df.truncate(before=start_date, after=end_date)
                # df = df.loc[(df.index >= start_date) & (df.index <= end_date)]
            elif start_date is not None:
                start_date = pd.to_datetime(start_date)
                df = df.truncate(before=start_date)
                # df = df.loc[df.index >= start_date]
            elif end_date is not None:
                end_date = pd.to_datetime(end_date)
                df = df.truncate(after=end_date)
                # df = df.loc[df.index <= end_date]

            # 然后在这基础上再做其他条件过滤
            if code_or_codes is not None:
                if isinstance(code_or_codes, str):
                    df = df.loc[df.code == code_or_codes]
                else:
                    df = df.loc[df.code.isin(code_or_codes)]

            if backs > 0:
                # 检查数据是否满足要求
                counts = df.groupby('code').size()
                counts = counts[counts.map(lambda x: x < backs + 1)]
                if len(counts) > 0:
                    # 对数据不足的部分单独处理，这部分数据不会很多

                    # 1. 从数据集中去掉这些股票的数据
                    df = df[~df.code.isin(counts.index)]

                    if not drop_suspended:
                        # 2. 需要从缓存或数据库中获取中间有停牌的数据
                        new_data = [df]
                        for code in counts.index:
                            # 首先尝试从缓存中直接获得
                            df_tmp, exists, full = self._get_backs_from_cache(code, end_date, backs, fields)
                            if exists:
                                # 这一天有数据
                                if full:
                                    # 缓存中的数据已经足够
                                    new_data.append(df_tmp)
                                else:
                                    # 缓存中的前置数据不够，需要从数据库中临时获取
                                    df_tmp = db.get_day_backs(code, end_date, backs, fields)
                                    if df_tmp is not None and len(df_tmp) == backs + 1:
                                        new_data.append(df_tmp)
                            else:
                                # 这一天没数据，忽略该股票
                                pass
                            del df_tmp

                        del counts

                        if len(new_data) > 1:  # 将重新获取的数据合并到数据集中
                            df = pd.concat(new_data, copy=False)
                            del new_data

                            # 需要重新按照日期排序
                            # df.sort_index(inplace=True)

        return df


cached_db_day = CachedDatabaseDay()
