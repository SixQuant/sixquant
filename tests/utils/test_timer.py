# coding=utf-8

import unittest

from sixquant import option
from sixquant.utils.timer import RecycleTimer, TradingTimeTimer


class TestMethods(unittest.TestCase):
    def nothing(self, step):
        self.counter += step
        pass

    def test_recycle_timer(self):

        # 同步模式，可以指定运行次数
        timer = RecycleTimer(interval=0.1, target=self.nothing, max_times=5, align_to_minute=True)

        self.counter = 0
        timer.start(1)
        self.assertEqual(5, self.counter)

        # 异步模式
        self.counter = 0
        timer = RecycleTimer(interval=0.1, target=self.nothing, async=True, align_to_minute=True)
        timer.start(1)  # 启动了一个独立线程
        timer.stop()

        self.counter = 0
        timer = RecycleTimer(interval=0.1, target=self.nothing, async=True)
        timer.start(1)  # 启动了一个独立线程

        while True:
            if self.counter == 5:
                timer.pause()
                self.assertTrue(timer.is_paused())
                timer.resume()
                timer.stop()
                self.assertTrue(timer.is_stopped())
                break

        self.assertEqual(5, self.counter)

    def test_trading_timeTimer(self):
        option.is_trading_time_now = True
        timer = TradingTimeTimer(interval=0.1, target=self.nothing, max_times=5)

        self.counter = 0
        timer.start(1)
        self.assertEqual(5, self.counter)

        option.is_trading_time_now = False
        timer = TradingTimeTimer(interval=0.1, target=self.nothing, max_times=5, run_on_startup=True)

        self.counter = 0
        timer.start(1)
        self.assertEqual(1, self.counter)

        option.is_trading_time_now = None


if __name__ == '__main__':
    unittest.main()
