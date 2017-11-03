# coding=utf-8

import unittest

import os
import pandas as pd
from sixquant import dataframe_to_html_file
from sixquant.fileutils import get_temp_filename


class TestMethods(unittest.TestCase):
    def test_dataframe_to_html(self):
        tmp_filename = get_temp_filename('test_tmp.html')
        df = pd.DataFrame(data=[[1, 2, 3]], columns=['a', 'b', 'c'])
        dataframe_to_html_file(df, tmp_filename, 'title')
        self.assertTrue(os.path.exists(tmp_filename))
        os.remove(tmp_filename)


if __name__ == '__main__':
    unittest.main()
