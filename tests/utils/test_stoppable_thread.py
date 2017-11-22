# coding=utf-8

import unittest

import time

from sixquant.utils.stoppable_thread import StoppableThread


class TestMethods(unittest.TestCase):
    def test_stoppable_thread(self):
        """Test :func:`stoppable_thread()`."""

        def _run(a, b):
            self.assertEqual(1, a)

        t = StoppableThread(target=_run, args=(1, 2))
        t.start()
        time.sleep(1)
        t.pause()
        t.resume()
        self.assertFalse(t.is_paused())
        t.pause()
        self.assertTrue(t.is_paused())
        self.assertFalse(t.is_stopped())
        t.stop()
        self.assertTrue(t.is_stopped())


if __name__ == '__main__':
    unittest.main()
