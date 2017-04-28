# encoding: utf-8

"""
twinado server.utils

~~~~~~

twinado server 的功能辅助模块

架构如下:
    utils.data_type: 数据类型和类型检查相关

"""

import uuid
from functools import wraps


def gen_uuid():
    return uuid.uuid4().hex


def silent_return_none(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            rv = func(*args, **kwargs)
        except Exception:
            rv = None
        return rv

    return wrapper
