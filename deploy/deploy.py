# encoding: utf-8

"""
twinado deploy.deploy

~~~~~~

twinado 的部署流程

"""

from deploy.utils import StageManager, TaskManager

from deploy.tasks.app import app_restart
from deploy.tasks.python import python_install_requirements
from deploy.tasks.repo import repo_pull, repo_run_test, repo_upgrade_database

deploy_manager = TaskManager("deploy")


def deploy(role, stage):
    stage = StageManager.retrieve(stage)
    deploy_manager.setup_env(role, stage)

    deploy_manager.run_all()


@deploy_manager.register
def unittest():
    repo_run_test()


@deploy_manager.register
def update_repo():
    repo_pull()


@deploy_manager.register
def update_python_package():
    python_install_requirements()


@deploy_manager.register
def update_database():
    repo_upgrade_database()


@deploy_manager.register
def restart_app():
    app_restart()
