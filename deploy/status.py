# encoding: utf-8

"""
twinado deploy.status

~~~~~~

twinado 服务端状态

"""

from deploy.tasks.app import app_status
from deploy.tasks.nginx import nginx_status
from deploy.utils import StageManager, TaskManager

status_manager = TaskManager("status")


def status(role, stage, targets="all"):
    stage = StageManager.retrieve(stage)
    status_manager.setup_env(role, stage)

    targets = status_manager.confirm(targets)
    for target in targets:
        target_func = status_manager.retrieve(target)
        if target_func is not None:
            target_func()


@status_manager.register
def app():
    app_status()


@status_manager.register
def nginx():
    nginx_status()
