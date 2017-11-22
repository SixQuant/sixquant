# coding=utf-8

from threading import Event, Thread


class StoppableThread(Thread):
    """
    支持暂停和停止的线程类，Python原生不支持这些特性
    """

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)

        self.__not_pause_flag = Event()  # 用于暂停线程
        self.__not_pause_flag.set()
        self.__running_flag = Event()  # 用于停止线程
        self.__running_flag.set()

    def pause(self):
        """暂停执行, 让线程阻塞"""
        self.__not_pause_flag.clear()

    def resume(self):
        """恢复执行，让线程停止阻塞"""
        self.__not_pause_flag.set()

    def is_paused(self):
        """线程是否处理暂停状态"""
        return not self.__not_pause_flag.is_set()

    def stop(self):
        """停止运行，结束线程"""
        self.__not_pause_flag.set()  # 将线程从暂停状态恢复, 如果已经暂停的话
        self.__running_flag.clear()  # 停止运行

    def is_stopped(self):
        """线程是否处于停止状态"""
        return not self.__running_flag.is_set()

    def run(self):
        """
        重载父类方法
        :return:
        """
        try:
            while self.__running_flag.isSet():
                self.__not_pause_flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
                if self._target:
                    self._target(*self._args, **self._kwargs)

        finally:
            # Avoid a refcycle if the thread is running a function with
            # an argument that has a member that points to the thread.
            del self._target, self._args, self._kwargs
