# coding=utf-8

import logging.config


class Logger(object):
    logging_conf = __file__[:len(__file__) - len('logger.py')] + 'logging.conf'
    logging.config.fileConfig(logging_conf)
    logging.getLogger("requests").setLevel(logging.WARNING)  # disable log messages from the Requests library

    def __init__(self):
        self.verbose = False

    def config(self, fname, defaults=None, disable_existing_loggers=True):
        logging.config.fileConfig(fname, defaults=defaults, disable_existing_loggers=disable_existing_loggers)

    def get(self, name=None):
        return logging.getLogger(name)


logger = Logger()
