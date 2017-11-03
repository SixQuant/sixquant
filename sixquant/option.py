# coding=utf-8

import os


class Option(object):
    def __init__(self, path='./data'):
        self._data_path = path
        self.debugging = False  # 是否处于调试状态，让 is_trading_time 等函数直接返回 True
        self.verbose = False

    def set_data_path(self, path='./data'):
        self._data_path = path

    def get_data_path(self):
        return self._data_path

    def get_data_filename(self, subdir, filename=None):
        """
        返回数据文件名称
        :return:
        """
        if filename is None:
            filename = subdir
            subdir = None

        path = self.get_data_path()
        if subdir is None or len(subdir) == 0:
            return path + os.sep + filename
        else:
            return path + os.sep + subdir + os.sep + filename


option = Option()
