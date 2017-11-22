# coding=utf-8

import unittest
from sixquant import get_concepts_no_black, get_concepts_list_no_black, get_concepts_list


class TestMethods(unittest.TestCase):
    def test_get_concepts_list_no_black(self):
        self.assertIsNotNone(get_concepts_list_no_black())

    def test_get_concepts_no_black(self):
        self.assertIsNotNone(get_concepts_no_black('002136'))
        self.assertIsNone(get_concepts_no_black('------'))

    def test_get_concepts_list(self):
        self.assertIsNotNone(get_concepts_list(black_list=['不知所谓']))


if __name__ == '__main__':
    unittest.main()
