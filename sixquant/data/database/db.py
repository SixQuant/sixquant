# coding=utf-8

import os
import sqlite3 as lite
import pandas as pd
import atexit

from ...option import option
from ...utils.datetime_utils import to_date_str


class Database(object):
    """
    数据库支持（SQLite3）
    """

    def __init__(self, filename=option.get_data_filename('day.six')):
        self.con = None
        self.filename = filename

        atexit.register(self.close)

    def initialize(self):
        if self.con is None:
            exists = os.path.exists(self.filename)
            self.con = lite.connect(self.filename)

            if not exists:
                self.create_tables()

    def get_filename(self):
        return self.filename

    def close(self):
        if self.con is not None:
            self.con.close()
            self.con = None

    def create_tables(self):
        self.create_table_basic_name()
        self.create_table_day()

    def create_table_basic_name(self):
        sql = """
            CREATE TABLE basic_name(
                date DATE NOT NULL,
                code VARCHAR(10) NOT NULL,
                name VARCHAR(8) NOT NULL
                );
        """
        cur = self.con.cursor()
        cur.execute(sql)

        sql = 'CREATE UNIQUE INDEX ix_basic_name_date_code ON basic_name(date,code);'
        cur.execute(sql)

        self.con.commit()

    def create_table_day(self):
        sql = """
            CREATE TABLE day(
                date DATE NOT NULL,
                code VARCHAR(10) NOT NULL,
                open FLOAT,
                close FLOAT,
                high FLOAT,
                low FLOAT,
                volume FLOAT,
                amount FLOAT,
                pt_turn FLOAT,
                money_huge FLOAT,
                money_large FLOAT,
                money_medium FLOAT,
                money_small FLOAT,
                factor FLOAT
                );
        """
        cur = self.con.cursor()
        cur.execute(sql)

        sql = 'CREATE UNIQUE INDEX ix_day_date_code ON day(date,code);'
        cur.execute(sql)

        self.con.commit()

    def get_connection(self):
        if self.con is None:
            self.initialize()

        return db.con

    def put_basic_name(self, df):
        """
        合并日线数据
        :param df:
        :return:
        """
        if self.con is None:
            self.initialize()

        insert_sql = 'INSERT INTO basic_name(date,code,name)VALUES(?,?,?)'
        update_sql = 'UPDATE basic_name SET name=? WHERE date=? AND code=?'

        cur = self.con.cursor()
        for date, r in df.iterrows():
            date = to_date_str(date)
            try:
                params = (date, r['code'], r['name'],)
                cur.execute(insert_sql, params)
            except lite.IntegrityError:
                params = (r['name'], date, r['code'],)
                cur.execute(update_sql, params)

        self.con.commit()

    def get_basic_name(self, code, date=None):
        """
        检索日线数据
        :param code:
        :param date:
        :return:
        """
        if self.con is None:
            self.initialize()

        sql = 'SELECT name FROM basic_name WHERE date<=? ORDER BY date LIMIT 1'
        params = (date,)
        df = pd.read_sql_query(sql, self.con, params=params, index_col='date')
        df.index.name = None
        df.index = pd.to_datetime(df.index)
        return df

    def get_stocks(self, date=None):
        """
        检索日线数据
        :param date:
        :return:
        """
        if self.con is None:
            self.initialize()

        sql = 'SELECT code FROM basic_name WHERE date<=? ORDER BY date LIMIT 1'
        params = (date,)
        df = pd.read_sql_query(sql, self.con, params=params, index_col='date')
        df.index.name = None
        df.index = pd.to_datetime(df.index)
        return df

    def put_day(self, df):
        """
        合并日线数据
        :param df:
        :return:
        """
        if self.con is None:
            self.initialize()

        insert_sql = 'INSERT INTO day(date'
        for column in df.columns:
            insert_sql += ',' + column
        insert_sql += ') VALUES(?' + (',?' * len(df.columns)) + ')'

        update_sql = 'UPDATE day SET '
        for column in df.columns:
            if column != 'code':
                update_sql += column + '=?,'
        update_sql = update_sql[:len(update_sql) - 1] + ' WHERE date=? AND code=?'

        cur = self.con.cursor()
        for date, r in df.iterrows():
            date = to_date_str(date)
            try:
                params = (date,) + tuple(r)
                cur.execute(insert_sql, params)
            except lite.IntegrityError:
                code = r['code']
                del r['code']
                params = tuple(r) + (date, code,)
                cur.execute(update_sql, params)

        self.con.commit()

    def get_day_all(self, start_date=None, end_date=None, fields=None):
        """
        检索日线数据
        :param start_date:
        :param end_date:
        :param fields:
        :return: Pandas DataFrame
        """
        if self.con is None:
            self.initialize()

        if fields is None or fields == '':
            sql = 'SELECT * FROM day'
        else:
            sql = 'SELECT ' + (','.join(fields)) + ',date FROM day'

        if start_date is not None and end_date is not None:
            sql += ' WHERE date>=? and date<=?'
            params = (start_date, end_date,)
        elif start_date is not None:
            sql += ' WHERE date>=?'
            params = (start_date,)
        elif end_date is not None:
            sql += ' WHERE date<=?'
            params = (end_date,)
        else:
            params = None

        # sql += ' ORDER BY date'

        df = pd.read_sql_query(sql, self.con, params=params)
        df.date = pd.to_datetime(df.date)

        # Pandas MultiIndex DataFrame
        # df.set_index(['code', 'date'], inplace=True)
        df.set_index('date', inplace=True)
        df.index.name = None

        # TODO 测试一下 df.sort_index 后性能是否有所提升
        df.sort_index(axis=0, ascending=True, inplace=True)  # 按照日期从小到大排列，与米宽等一致

        return df

    def get_day_backs(self, code, date, backs, fields):
        """
        从数据库中临时获取 date 日往前 backs 个数据
        :param code:
        :param date:
        :param backs:
        :param fields:
        :return: df
        """
        if self.con is None:
            self.initialize()

        sql = 'SELECT date,' + (','.join(fields)) + ' FROM day WHERE date<=? and code=? ORDER BY date DESC LIMIT ?'
        params = (to_date_str(date), code, backs,)

        df = pd.read_sql_query(sql, self.con, params=params)
        df.date = pd.to_datetime(df.date)

        df.set_index('date', inplace=True)
        df.index.name = None

        df.sort_index(axis=0, ascending=True, inplace=True)  # 按照日期从小到大排列，与米宽等一致

        return df


db = Database()
