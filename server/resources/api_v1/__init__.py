# encoding: utf-8

"""
twinado server.resource.api_v1

~~~~~~

twinado server 的 api_v1 业务模块

架构如下:
    api_v1.main: 基础 api 业务
    api_v1.user: 用户相关 api 业务

"""

from server.application import API

apiv1 = API(name='api_v1', prefix='/api/v1')

from .main import main
from .user import user
