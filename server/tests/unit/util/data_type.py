# encoding: utf-8

"""
twinado server.tests.unit.util.data_type

~~~~~~

twinado server 测试 data_type 下各个功能

"""

import json

from server.tests.unit import UtilTestBase
from server.utils.data_type import check_data_type, force_dict_type
from server.utils.data_type import DataTypeError, IllegalDictData


class DataTypeUtilTest(UtilTestBase):
    def __init__(self, *args, **kwargs):
        super(DataTypeUtilTest, self).__init__(*args, **kwargs)

    def test_data_type_check(self):
        self.assertTrue(check_data_type(1, int))
        self.assertTrue(check_data_type(1.0, float))
        self.assertTrue(check_data_type("1", str))
        self.assertTrue(check_data_type({"a": 1}, dict))
        self.assertTrue(check_data_type([1, 2], list))
        self.assertTrue(check_data_type((1, 2), tuple))
        self.assertTrue(check_data_type({1, 2}, set))

        with self.assertRaises(DataTypeError):
            check_data_type([1, 2], tuple)

    def test_force_dict_type(self):
        data = {"name": "name", "age": 22}
        self.assertEqual(data, force_dict_type(data))

        dict_str = json.dumps(data)
        dict_result = force_dict_type(dict_str)
        self.assertEqual(data["name"], dict_result["name"])
        self.assertEqual(data["age"], dict_result["age"])

        data = "[1, 2]"
        with self.assertRaises(IllegalDictData):
            force_dict_type(data)
