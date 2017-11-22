# coding=utf-8

import os


class Option(object):
    def __init__(self, path=None):
        if path is None:
            path = os.getenv("SIXQUANT_DATA_DIR")
            if path is None or "" == path:
                path = os.path.abspath(os.path.expanduser('~/.sixquant'))

        self.env = 'development' if os.path.exists('../../sixquant.egg-info') else 'product'

        self._data_path = path
        self.debugging = False  # 是否处于调试状态
        self.is_trading_time_now = None  # 是否让 is_trading_time 函数直接返回 True
        self.verbose = False

        self.enable_caching_day = True  # 是否缓存日线数据
        self.enable_caching = True  # 是否缓存

    def set_data_path(self, path):
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

    def is_development_env(self):
        """当前是否处于开发环境"""
        return self.env == 'development'


option = Option()
