# coding=utf-8

from .utils.daily_cache import daily_cache
from .utils.daily_func_cache_watcher import daily_func_cache_watcher
from .data.database.cached_db_day import cached_db_day


class Cache(object):
    """
    缓存控制类
    """

    def __init__(self):
        pass

    def reset_day_cache(self):
        """
        重置日线缓存数据
        """
        cached_db_day.reset()

    def reset_daily_cache(self):
        """
        重置日化数据缓存池
        """
        daily_cache.reset()

    def reset_daily_func_cache(self):
        """
        重置日化函数缓存池
        """
        daily_func_cache_watcher.reset()

    def reset(self):
        """
        重置所有缓存
        """
        self.reset_day_cache()
        self.reset_daily_cache()
        self.reset_daily_func_cache()


cache = Cache()
