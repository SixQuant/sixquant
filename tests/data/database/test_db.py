# coding=utf-8

import unittest

import os
import pandas as pd

from sixquant import option
from sixquant.data.database.db import Database


class TestMethods(unittest.TestCase):
    def test_db(self):
        filename = option.get_data_filename('day-unit-test.six')
        if os.path.exists(filename):
            os.remove(filename)

        db = Database(filename)
        self.assertEqual(filename, db.get_filename())
        db.get_connection()
        db.close()

        db.get_day_all()
        db.close()

        db.get_day_backs('0000001', date='2017-11-01', backs=1, fields=['open'])
        db.close()

        try:
            df = pd.DataFrame(
                [['000001', 11.716],
                 ['000001', 15.716],
                 ['000001', 115.716]
                 ],
                index=['2017-10-30',
                       '2017-10-31',
                       '2017-11-01'
                       ],
                columns=['code', 'factor'])
            df.index = pd.to_datetime(df.index)
            db.put_day(df)

            df = pd.DataFrame(
                [['000001', 1],
                 ['000001', 2],
                 ['000001', 3]
                 ],
                index=['2017-10-30',
                       '2017-10-31',
                       '2017-11-01'
                       ],
                columns=['code', 'close'])
            df.index = pd.to_datetime(df.index)
            db.put_day(df)

            df = db.get_day_all(fields=['code', 'close', 'factor'])

            self.assertTrue(isinstance(df, pd.DataFrame))
            self.assertEqual(3, len(df))
            self.assertEqual(['2017-10-30', '2017-10-31', '2017-11-01'], df.index.strftime('%Y-%m-%d').tolist())
            self.assertEqual([['000001', 1.0, 11.716],
                              ['000001', 2.0, 15.716],
                              ['000001', 3.0, 115.716]], df.values.tolist())

            df = db.get_day_all(start_date='2017-10-30')
            self.assertEqual(3, len(df))
            df = db.get_day_all(end_date='2017-11-01')
            self.assertEqual(3, len(df))
            df = db.get_day_all(start_date='2017-10-30', end_date='2017-11-01')
            self.assertEqual(3, len(df))

        finally:
            db.close()

        if os.path.exists(filename):
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()
