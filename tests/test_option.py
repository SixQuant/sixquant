# coding=utf-8

import unittest
from sixquant import option


class TestMethods(unittest.TestCase):
    def test_get_data_filename(self):
        path = option.get_data_path()
        option.set_data_path('./xyz')
        self.assertEqual('./xyz', option.get_data_path())
        option.set_data_path(path)
        self.assertEqual('./data', option.get_data_path())

        self.assertEqual('./data/abc', option.get_data_filename('abc'))
        self.assertEqual('./data/abc/123.csv', option.get_data_filename('abc', '123.csv'))


if __name__ == '__main__':
    unittest.main()
