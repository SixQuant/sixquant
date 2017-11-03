# coding=utf-8

import unittest
from sixquant import logger


class TestMethods(unittest.TestCase):
    def test_get(self):
        logging_conf = __file__[:len(__file__) - len('test_logger.py')] + '/../sixquant/logging.conf'
        logger.config(logging_conf)
        self.assertIsNotNone(logger.get(__name__))


if __name__ == '__main__':
    unittest.main()
