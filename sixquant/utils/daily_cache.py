# coding=utf-8

import datetime
import threading
import time

from .logger import logger


class DailyCache(object):
    """
    每日零点自动重置的缓存器
    """

    def __init__(self):
        self._dict = {}
        self._daemon_start()

    def _daemon_start(self):
        """启动守护线程"""
        t = threading.Thread(target=self._daemon_run)
        t.setName('DailyCache')
        t.setDaemon(True)
        t.start()

    def _daemon_run(self):
        """守护线程主函数"""
        # 每日 0 点清理函数调用缓存
        next_run_time = datetime.date.today().strftime('%Y-%m-%d') + ' ' + '00:00:01'
        next_run_time = datetime.datetime.strptime(next_run_time, '%Y-%m-%d %H:%M:%S')
        next_run_time = next_run_time + datetime.timedelta(days=1)
        while True:
            if datetime.datetime.now() >= next_run_time:
                next_run_time = next_run_time + datetime.timedelta(days=1)
                self.reset()
            time.sleep(1)

    def reset(self):
        """
        清理日化数据缓存
        """
        log = logger.get(__name__)
        log.debug('reset daily data cache.')

        self._dict = {}

    def set(self, key, value):
        self._dict[key] = value

    def get(self, key):
        try:
            return self._dict[key]
        except KeyError:
            return None


daily_cache = DailyCache()
