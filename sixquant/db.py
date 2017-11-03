# coding=utf-8

import os
import sqlite3 as lite
import pandas as pd
import atexit

from .option import option
from .utils import to_date_str


class Database(object):
    """
    数据库支持（SQLite3）
    """

    def __init__(self):
        self.con = None

    def initialize(self):
        filename = option.get_data_filename('day.six')
        exists = os.path.exists(filename)
        self.con = lite.connect(filename)

        atexit.register(self.close)

        if not exists:
            self.create_tables()

    def close(self):
        if self.con is not None:
            self.con.close()
            self.con = None

    def create_tables(self):
        self.create_table_day()

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

    def get_day(self, code, start_date=None, end_date=None, fields=None):
        """
        检索日线数据
        :param code:
        :param start_date:
        :param end_date:
        :param fields:
        :return:
        """
        if self.con is None:
            self.initialize()

        if fields is None:
            sql = 'SELECT * FROM day'
        else:
            sql = 'SELECT date,' + (','.join(fields)) + ' FROM day'

        if start_date is not None and end_date is not None:
            sql += ' WHERE date>=? and date<=? and code=?'
            params = (start_date, end_date, code,)
        elif start_date is not None:
            sql += ' WHERE date>=? and code=?'
            params = (start_date, code,)
        elif end_date is not None:
            sql += ' WHERE date<=? and code=?'
            params = (end_date, code,)
        else:
            sql += ' WHERE code=?'
            params = (code,)

        sql += ' ORDER BY date'

        df = pd.read_sql_query(sql, self.con, params=params, index_col='date')
        df.index.name = None
        df.index = pd.to_datetime(df.index)
        return df


db = Database()
