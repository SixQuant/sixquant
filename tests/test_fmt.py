# coding=utf-8

import unittest
from sixquant import fmt_round_number, fmt_file_size


class TestMethods(unittest.TestCase):
    def test_fmt_round_number(self):
        """Test :func:`fmt_round_number()`."""
        self.assertEqual('1', fmt_round_number(1))
        self.assertEqual('1', fmt_round_number(1.0))
        self.assertEqual('1.00', fmt_round_number(1, keep_width=True))
        self.assertEqual('3.14', fmt_round_number(3.141592653589793))

    def test_fmt_file_size(self):
        """Test :func:`fmt_file_size()`."""
        self.assertEqual('0', fmt_file_size(0))
        self.assertEqual('1', fmt_file_size(1))
        self.assertEqual('42', fmt_file_size(42))
        self.assertEqual('1K', fmt_file_size(1024 ** 1))
        self.assertEqual('1M', fmt_file_size(1024 ** 2))
        self.assertEqual('1G', fmt_file_size(1024 ** 3))
        self.assertEqual('1T', fmt_file_size(1024 ** 4))
        self.assertEqual('1P', fmt_file_size(1024 ** 5))
        self.assertEqual('45K', fmt_file_size(1024 * 45))
        self.assertEqual('2.9T', fmt_file_size(1024 ** 4 * 2.9))


if __name__ == '__main__':
    unittest.main()
