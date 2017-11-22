# coding=utf-8

import os
import unittest

import pandas as pd

from sixquant import dataframe_to_html_file, html_get_pt_price_color
from sixquant.utils.file_utils import get_temp_filename


class TestMethods(unittest.TestCase):
    def test_html_get_pt_price_color(self):
        self.assertEqual('bcr7', html_get_pt_price_color(+8))
        self.assertEqual('bcr5', html_get_pt_price_color(+5))
        self.assertEqual('bcr3', html_get_pt_price_color(+3))
        self.assertEqual('bcr1', html_get_pt_price_color(+1))

        self.assertEqual('bcg7', html_get_pt_price_color(-8))
        self.assertEqual('bcg5', html_get_pt_price_color(-5))
        self.assertEqual('bcg3', html_get_pt_price_color(-3))
        self.assertEqual('bcg1', html_get_pt_price_color(-1))

        self.assertEqual('bcr0', html_get_pt_price_color(0))


if __name__ == '__main__':
    unittest.main()
