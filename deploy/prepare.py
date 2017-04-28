# encoding: utf-8

"""
twinado deploy.prepare

~~~~~~

twinado 服务端环境准备流程, 用来安装各种依赖(dependency)

"""

from deploy.tasks.python import python_prepare
from deploy.tasks.repo import repo_prepare
from deploy.tasks.supervisor import supervisor_prepare
from deploy.tasks.nginx import nginx_prepare
from deploy.utils import StageManager, TaskManager

dependency_manager = TaskManager("prepare")


def prepare(role, stage, dependencies="all"):
    stage = StageManager.retrieve(stage)
    dependency_manager.setup_env(role, stage)

    dependencies = dependency_manager.confirm(dependencies)

    for depend in dependencies:
        function_to_setup_dependency = dependency_manager.retrieve(depend)
        if function_to_setup_dependency is not None:
            function_to_setup_dependency()


@dependency_manager.register
def python():
    python_prepare()


@dependency_manager.register
def repo():
    repo_prepare()


@dependency_manager.register
def nginx():
    nginx_prepare()


@dependency_manager.register
def supervisor():
    supervisor_prepare()
