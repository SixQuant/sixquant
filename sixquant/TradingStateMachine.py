# coding=utf-8

from .utils import is_trading_time


class TradingStateMachine(object):
    """
    交易时间状态机
    """

    def __init__(self):
        self.first_time = True
        self.last_time = False

    def is_trading(self):
        """
        保证至少会被执行一次，收盘后会再被执行一次
        :return:
        """
        in_trading_time = is_trading_time()
        if self.first_time or in_trading_time or self.last_time:
            self.first_time = False
            if self.last_time:
                self.last_time = False
            elif not in_trading_time:
                self.last_time = True

            return True
        return False
