# coding=utf-8

import unittest
from sixquant import option
from sixquant.option import Option
import os


class TestMethods(unittest.TestCase):
    def test_get_data_filename(self):
        path = os.getenv("SIXQUANT_DATA_DIR")
        os.environ["SIXQUANT_DATA_DIR"] = ""
        self.assertTrue(Option().get_data_path().endswith('/.sixquant'))
        if path is not None:
            os.environ["SIXQUANT_DATA_DIR"] = path

        path = option.get_data_path()

        option.set_data_path('./xyz')
        self.assertEqual('./xyz', option.get_data_path())

        self.assertEqual('./xyz/abc', option.get_data_filename('abc'))
        self.assertEqual('./xyz/abc/123.csv', option.get_data_filename('abc', '123.csv'))

        option.set_data_path(path)
        self.assertEqual(path, option.get_data_path())

        option.is_development_env()


if __name__ == '__main__':
    unittest.main()
