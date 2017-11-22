# coding=utf-8

import os
import logging.config

urllib3_log = logging.getLogger("urllib3")
urllib3_log.setLevel(logging.CRITICAL)

requests_log = logging.getLogger("requests")
requests_log.addHandler(logging.NullHandler())
requests_log.propagate = False


# logging.getLogger("requests").setLevel(logging.WARNING)  # disable log messages from the Requests library

class Logger(object):
    _logging_conf = __file__[:len(__file__) - len('logger.py')] + '../logging.conf'
    if os.path.exists(_logging_conf):
        logging.config.fileConfig(_logging_conf)

    def __init__(self):
        self.verbose = False

    def config(self, fname, defaults=None, disable_existing_loggers=True):
        logging.config.fileConfig(fname, defaults=defaults, disable_existing_loggers=disable_existing_loggers)

    def get(self, name=None):
        return logging.getLogger(name)


logger = Logger()
