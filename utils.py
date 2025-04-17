# pylint: disable=C0103
"""
编写了一些与算法本身无关但能便于使用的函数工具
"""

import datetime

from materials import *


def timestr():
    return str(datetime.datetime.now())

