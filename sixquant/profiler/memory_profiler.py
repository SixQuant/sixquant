# coding=utf-8

import os
import psutil

from ..utils.fmt import fmt_file_size


def get_used_memory_size():
    """
    返回实际使用的内存大小
    VSS - Virtual Set Size 虚拟耗用内存（包含共享库占用的内存）
    RSS - Resident Set Size 实际使用物理内存（包含共享库占用的内存）
    PSS - Proportional Set Size 实际使用的物理内存（比例分配共享库占用的内存）
    USS - Unique Set Size 进程独自占用的物理内存（不包含共享库占用的内存）
    一般来说内存占用大小有如下规律：VSS >= RSS >= PSS >= USS
    :return:
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss


def get_used_memory_size_str():
    return fmt_file_size(get_used_memory_size())
