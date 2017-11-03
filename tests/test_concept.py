# coding=utf-8

import unittest
from sixquant import get_concepts_no_black, get_concepts_list_no_black


class TestMethods(unittest.TestCase):
    def test_get_concepts_list_no_black(self):
        self.assertIsNotNone(get_concepts_list_no_black())

    def test_get_concepts_no_black(self):
        self.assertIsNotNone(get_concepts_no_black('000001'))
        self.assertIsNone(get_concepts_no_black('------'))


if __name__ == '__main__':
    unittest.main()
