# encoding: utf-8

"""
twinado deploy.tasks

~~~~~~

twinado 组建各个部署流程的基本任务模块

架构如下:
    tasks.app app 服务器相关的 task
    tasks.nginx nginx 环境相关的 task
    tasks.apt 系统软件包相关的 task
    task.git git 相关的 task
    tasks.python python 环境相关的 task
    tasks.repo 部署流程中代码仓环境相关的 task
    tasks.supervisor supervisor 相关的 task

"""

from deploy.tasks.app import *
from deploy.tasks.apt import *
from deploy.tasks.git import *
from deploy.tasks.nginx import *
from deploy.tasks.python import *
from deploy.tasks.repo import *
from deploy.tasks.supervisor import *
