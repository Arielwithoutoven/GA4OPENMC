# pylint: disable=C0103
"""
编写了一些与算法本身无关但能便于使用的函数工具
"""

import os
import time
from math import modf


def timestr():
    """return f"{date}'{stamp}" """
    stamp = str(modf(time.time())[0])[2:10]
    date = time.strftime("%Y%m%d'%H:%M:%S", time.localtime())
    return f"{date}'{stamp}"


def test():
    """test func"""


if __name__ == "__main__":
    print(os.sep)
    print(os.name)
    print(os.getenv("path"))
    print(os.getcwd())
    os.makedirs("." + os.sep + "Individuals" + os.sep + timestr())
