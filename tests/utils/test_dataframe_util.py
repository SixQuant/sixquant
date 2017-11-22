# coding=utf-8

import unittest

from sixquant import request_dataframe
from sixquant.constants import BUNDLE_SERVER_URL, BASICS_FILE


class TestMethods(unittest.TestCase):
    def test_request_dataframe(self):
        df = request_dataframe(BUNDLE_SERVER_URL + '/not_exists')
        self.assertIsNone(df)

        df = request_dataframe(BASICS_FILE)
        self.assertIsNotNone(df)


if __name__ == '__main__':
    unittest.main()
