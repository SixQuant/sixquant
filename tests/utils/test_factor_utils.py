# coding=utf-8

import unittest

import numpy as np
import pandas as pd

from sixquant.utils.factor_utils import get_relevant_factor


class TestMethods(unittest.TestCase):
    def test_get_relevant_factor(self):
        # 计算响应的复权因子数据

        # 1. 单个股票
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
        factor = get_relevant_factor(df['factor'])
        self.assertEqual(115.716, factor)

        # 2. 多个股票
        df = pd.DataFrame(
            [['000001', 122.716],
             ['000001', 15.716],
             ['000001', 115.716],
             ['600469', 3.637],
             ['600469', 1.637],
             ['600469', 2.637]
             ],
            index=['2017-10-30',
                   '2017-10-31',
                   '2017-11-01',
                   '2017-10-27',
                   '2017-10-30',
                   '2017-11-01'
                   ],
            columns=['code', 'factor'])
        df.index = pd.to_datetime(df.index)
        factor = get_relevant_factor(df[['code', 'factor']])
        self.assertTrue(isinstance(factor, np.ndarray))
        self.assertEqual(6, len(factor))
        self.assertEqual([115.716, 115.716, 115.716, 2.637, 2.637, 2.637], factor.tolist())


if __name__ == '__main__':
    unittest.main()
