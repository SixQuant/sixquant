# coding=utf-8

import threading
import time


class Timer(object):
    """
    定时回调
    """

    def __init__(self, interval, callback, async=False, daemon=True, async_thread_name='Timer'):
        """
        :param interval: 调用间隔
        :param callback: 回调函数
        :param async: 是否异步，异步则启动一个独立线程
        :param daemon: 线程是否是守护线程
        :param async_thread_name: 线程名称
       """
        self.interval = interval  # 每两次调用之间的最小间隔时间(秒)
        self.callback = callback
        self.async = async
        self.daemon = daemon
        self.async_thread_name = async_thread_name

    def start(self, *args, **kwargs):
        """
        启动
        """
        if self.async:
            self._async_daemon_start(*args, **kwargs)
        else:
            self._start(*args, **kwargs)

    def _async_daemon_start(self, *args, **kwargs):
        """启动守护线程"""
        t = threading.Thread(target=self._async_daemon_run, args=args, kwargs=kwargs)
        t.setName(self.async_thread_name)
        t.setDaemon(self.daemon)
        t.start()

    def _async_daemon_run(self, *args, **kwargs):
        """守护线程主函数"""
        self._start(*args, **kwargs)

    def _start(self, *args, **kwargs):
        """
        启动
        :param callback: 回调函数
        :param async: 是否启动一个独立守护线程， True 表示是
        :return:
        """

        # 交易时段内每 interval 秒1次回调函数

        prev_time = None
        while True:
            if prev_time is None or (time.time() - prev_time >= self.interval):
                prev_time = time.time()

                self.callback(*args, **kwargs)

            sleep_time = self.interval - (time.time() - prev_time)
            if sleep_time > 0:
                time.sleep(sleep_time)
