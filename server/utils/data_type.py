# encoding: utf-8

"""
twinado server.utils.data_type

~~~~~~

twinado server 的 数据类型和类型检查模块

"""

import json

DataError = type("DataError", (Exception,), {})

DataTypeError = type("DataTypeError", (DataError,), {})

IllegalDictData = type("IllegalDictData", (DataError,), {})


def check_data_type(data_value, data_type, exc=None):
    """ 检查 data_value 是否是 data_type 的类型, 如果不是, 抛出 exc

    :arg data_value 被检查的数据
    :arg data_type  被要求的数据类型
    :key exc        数据与类型不匹配时抛出的异常
    :return boolean
    """

    if exc is None:
        exc = DataTypeError("Data type Error!")

    if not isinstance(data_value, data_type):
        raise exc
    return True


def force_dict_type(data, exc=None):
    """ 强制转换 data 为 dict 类型, 如果转换失败, 抛出 exc
    :arg data 被检查的 data
    :key exc 转换失败时抛出的异常
    :return 转换后的数据
    """

    if exc is None:
        exc = IllegalDictData("data is not a dict and cannot be converted to dict")

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except ValueError:
            raise exc

    if isinstance(data, dict):
        return data
    else:
        raise exc
