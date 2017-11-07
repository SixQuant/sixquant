# coding=utf-8

import os
import platform
import tempfile


def file_size(filename):
    return os.path.getsize(filename)


def get_temp_dir():
    temp_dir = '/tmp' if platform.system() == 'Darwin' else tempfile.gettempdir()
    return temp_dir


def get_temp_filename(filename):
    temp_dir = get_temp_dir()
    return temp_dir + os.sep + filename
