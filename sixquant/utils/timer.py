# coding=utf-8

import time
import datetime
from .datetime_utils import is_trading_time_now
from .stoppable_thread import StoppableThread


def sleep_align_to_minute():
    """
    睡眠对齐到整点分钟
    """
    t = datetime.datetime.now()
    sleep_time = 60 - t.second
    if 0 < sleep_time < 60:
        time.sleep(sleep_time)


class RecycleTimer(object):
    """
    定时器
    """

    def __init__(self,
                 interval,
                 target,
                 async=False,
                 daemon=True,
                 max_times=-1,
                 align_to_minute=False,
                 async_thread_name='RecycleTimer'):
        """
        :param interval: 调用间隔, 每两次调用之间的最小间隔时间(秒)
        :param target: 回调函数
        :param async: 是否异步，异步则启动一个独立线程
        :param daemon: 线程是否是守护线程
        :param max_times: 运行次数，-1 表示无限
        :param align_to_minute: 是否对齐到分钟整点
        :param async_thread_name: 线程名称
        """
        self._interval = interval
        self._target = target
        self._async = async
        self._daemon = daemon
        self._max_times = max_times
        self._align_to_minute = align_to_minute
        self._async_thread_name = async_thread_name
        self._thread = None
        self.prev_time = None

    def _run(self, *args, **kwargs):
        """
        主函数: 可供子类重载
        """
        self._target(*args, **kwargs)

    def _timer_run(self, *args, **kwargs):
        """
        主函数
        """

        # 每 interval 秒1次回调函数
        if self.prev_time is None or (time.time() - self.prev_time >= self._interval):
            self.prev_time = time.time()

            self._run(*args, **kwargs)

        sleep_time = self._interval - (time.time() - self.prev_time)
        if sleep_time > 0:
            time.sleep(sleep_time)

    def _async_start(self, *args, **kwargs):
        """启动异步线程"""
        t = StoppableThread(target=self._timer_run,
                            args=args, kwargs=kwargs,
                            name=self._async_thread_name,
                            daemon=self._daemon)
        self._thread = t

        if self._align_to_minute:
            sleep_align_to_minute()

        t.start()

    def _sync_run(self, *args, **kwargs):
        if self._align_to_minute:
            sleep_align_to_minute()

        times = 0
        while True:
            self._timer_run(*args, **kwargs)

            times += 1
            if -1 != self._max_times and times == self._max_times:  # 指定了运行次数
                break

    def start(self, *args, **kwargs):
        """
        启动
        """
        if self._async:
            self._async_start(*args, **kwargs)
        else:
            self._sync_run(*args, **kwargs)

    def pause(self):
        """异步模式时使用：暂停执行, 让线程阻塞"""
        if self._thread is not None:
            self._thread.pause()

    def resume(self):
        """异步模式时使用：恢复执行，让线程停止阻塞"""
        if self._thread is not None:
            self._thread.resume()

    def is_paused(self):
        """异步模式时使用：线程是否处理暂停状态"""
        return self._thread is not None and self._thread.is_paused()

    def stop(self):
        """异步模式时使用：停止运行，结束线程"""
        if self._thread is not None:
            self._thread.stop()

    def is_stopped(self):
        """异步模式时使用：线程是否处于停止状态"""
        return self._thread is not None and self._thread.is_stopped()


class TradingTimeTimer(RecycleTimer):
    """
    只在交易时间运行的定时器
    """

    def __init__(self,
                 interval,
                 target,
                 async=False,
                 daemon=True,
                 max_times=-1,
                 align_to_minute=False,
                 async_thread_name='TradingTimeTimer',
                 run_on_startup=False):
        """
        :param interval: 调用间隔
        :param target: 回调函数
        :param async: 是否异步，异步则启动一个独立线程
        :param daemon: 线程是否是守护线程
        :param max_times: 运行次数，-1 表示无限
        :param align_to_minute: 是否对齐到分钟整点
        :param async_thread_name: 线程名称
        :param run_on_startup: 启动时运行一次，即即使交易时间未到也先运行一次
        """
        super(TradingTimeTimer, self).__init__(interval=interval,
                                               target=target,
                                               async=async,
                                               daemon=daemon,
                                               max_times=max_times,
                                               align_to_minute=align_to_minute,
                                               async_thread_name=async_thread_name)
        self._run_on_startup = run_on_startup
        self._first = True

    def _run(self, *args, **kwargs):
        """
        主函数: 可供子类重载
        """
        if is_trading_time_now():
            self._target(*args, **kwargs)
        elif self._first and self._run_on_startup:
            self._first = False
            self._target(*args, **kwargs)
