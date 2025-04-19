# pylint: disable=C0103
"""
编写了一些与算法本身无关但能便于使用的函数工具
"""

import datetime
import json
import os


def timestr():
    return str(datetime.datetime.now())


def json_serializer(obj, path):
    assert not os.path.exists(path)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)


def json_parser(path):
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        json.load(f)
