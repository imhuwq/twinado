# encoding: utf-8

"""
twinado server.tests

~~~~~~

twinado server 的测试模块

架构如下:
    tests.unit: 单元测试模块

"""

import unittest
import importlib


class UnitTest:
    def __init__(self, name="."):
        if name == ".":
            name = "unit"
            module_name = "server.tests"
        else:
            module_name = "server.tests.unit"

        self.name = name
        self.module = importlib.import_module(module_name)

    def run(self):
        tests = unittest.TestLoader().loadTestsFromName(self.name, module=self.module)
        unittest.TextTestRunner(verbosity=2, failfast=True).run(tests)


from server.tests.unit import *
