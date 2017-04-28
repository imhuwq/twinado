# encoding: utf-8

"""
twinado deploy

~~~~~~

twinado 部署, 基于 python3 的 fabric3

架构如下:
    deploy.config: 部署流程的控制变量
    deploy.deploy: 对 twinado 进行部署
    deploy.prepare: 构建 twinado 服务端环境
    deploy.status: 观察服务器上的状态
    deploy.tasks: 组建各个流程的基本任务模块
"""

from deploy.config import *
from deploy.deploy import *
from deploy.prepare import *
from deploy.status import *
