# encoding: utf-8

"""
twinado server.tests.unit.app

~~~~~~

twinado server application 基础功能单元测试模块

架构如下:
    app.app_basic: 测试 app 核心功能
    app.api: 测试 api 功能
    app.login: 测试登录功能
    app.session: 测试 session 功能
    app.xsrf: 测试 xsrf 功能

"""

from server.tests.unit.app.app_basic import *
from server.tests.unit.app.api import *
from server.tests.unit.app.login import *
from server.tests.unit.app.session import *
from server.tests.unit.app.xsrf import *
