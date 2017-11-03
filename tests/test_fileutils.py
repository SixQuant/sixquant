# coding=utf-8

import unittest

import os

from sixquant.fileutils import file_size, get_temp_dir, get_temp_filename


class TestMethods(unittest.TestCase):
    def test_file_size(self):
        self.assertEqual(518, file_size(__file__))

    def test_get_temp_dir(self):
        self.assertIsNotNone(get_temp_dir())

    def test_file_size(self):
        temp_dir = get_temp_dir()
        self.assertEqual(temp_dir + os.sep + '123.tmp', get_temp_filename('123.tmp'))


if __name__ == '__main__':
    unittest.main()
