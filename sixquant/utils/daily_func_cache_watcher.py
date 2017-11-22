# coding=utf-8

import datetime
import threading
import time

from ..utils.logger import logger


class DailyFuncCacheWatcher(object):
    """
    函数调用缓存守护者，用来每日0点重置所有函数调用缓存
    """

    def __init__(self):
        self._lru_cache_func_dict = {}
        self._daemon_start()

    def _daemon_start(self):
        """启动守护线程"""
        t = threading.Thread(target=self._daemon_run)
        t.setName('DailyFuncCacheWatcher')
        t.setDaemon(True)
        t.start()

    def _daemon_run(self):
        """守护线程主函数"""
        # 每日 0 点清理函数调用缓存
        next_run_time = datetime.datetime.strptime(
            datetime.date.today().strftime('%Y-%m-%d') + ' ' + '00:00:01',
            '%Y-%m-%d %H:%M:%S')
        next_run_time = next_run_time + datetime.timedelta(days=1)
        while True:
            if datetime.datetime.now() >= next_run_time:
                next_run_time = next_run_time + datetime.timedelta(days=1)
                self.reset()
            time.sleep(1)

    def reset(self):
        """
        清理日化函数缓存
        :return:
        """
        log = logger.get(__name__)
        log.debug('reset daily func cache.')

        for (k, func) in self._lru_cache_func_dict.items():
            if hasattr(func, 'cache_clear'):
                func.cache_clear()

    def watch_lru_cache(self, func):
        """
        监控缓存函数，每天重置缓存
        :param func:
        :return:
        """
        if func.__name__ not in self._lru_cache_func_dict:
            self._lru_cache_func_dict[func.__name__] = func


daily_func_cache_watcher = DailyFuncCacheWatcher()
