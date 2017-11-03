# coding=utf-8

import time
import datetime
import threading
from .logger import logger


class DailyCache(object):
    """
    每日零点自动重置的缓存器
    """

    def __init__(self):
        self._dict = {}
        self._today_key = 0
        self._daemon_start()

    def _daemon_start(self):
        """启动守护线程"""
        t = threading.Thread(target=self._daemon_run)
        t.setName('DailyCache')
        t.setDaemon(True)
        t.start()

    def _daemon_run(self):
        """守护线程主函数
        :return:
        """
        try:
            # 每日 0 点清理函数调用缓存
            next_run_time = datetime.date.today().strftime('%Y-%m-%d') + ' ' + '00:00:01'
            next_run_time = datetime.datetime.strptime(next_run_time, '%Y-%m-%d %H:%M:%S')
            next_run_time = next_run_time + datetime.timedelta(days=1)
            while True:
                if datetime.datetime.now() >= next_run_time:
                    next_run_time = next_run_time + datetime.timedelta(days=1)
                    self.reset()
                time.sleep(1)
        except SystemExit:
            pass

    @property
    def today_key(self):
        """
        Return the today's key
        """
        return self._today_key

    def reset(self):
        """
        清理函数缓存
        :return:
        """
        log = logger.get(__name__)
        log.debug('daily reset cache.')

        self._dict = {}
        self._today_key = int(time.time() * 100)

    def set(self, key, value):
        self._dict[key] = value

    def get(self, key):
        try:
            return self._dict[key]
        except KeyError:
            return None


daily_cache = DailyCache()
