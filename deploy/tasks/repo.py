# encoding: utf-8

"""
twinado deploy.tasks.repo

~~~~~~

twinado 部署流程中代码仓环境相关的 task

"""

from fabric.api import run, put, env, local
from fabric.contrib.files import exists

from deploy.config import *
from deploy.tasks.git import git_prepare
from deploy.tasks.python import python_install_requirements


def repo_prepare():
    """ 准备代码仓环境 """
    git_prepare()
    repo_pull()
    repo_config()
    repo_install_requirements()
    repo_upgrade_database()


def repo_pull():
    """ 拉取最新代码 """
    if not exists(application_path):
        run("git clone {0} {1}".format(application_repo, application_path))
    else:
        run("cd {0} && git pull origin {1}".format(application_path, env.stage.branch))


def repo_config():
    """ 代码仓配置文件 """
    if not exists(config_path):
        run("mkdir -p {0}".format(config_path))
    put(local_application_config, application_conf)

    if exists(application_conf_link):
        run("rm {0}".format(application_conf_link))
    run("ln -s {0} {1}".format(application_conf, application_conf_link))


def repo_install_requirements():
    """ 代码仓依赖包 """
    python_install_requirements()


def repo_upgrade_database():
    """ 升级数据库 """
    run("cd {0}/server && {1} upgrade head".format(application_path, alembic_exec))


def repo_status():
    """ 代码仓当前版本 """
    pass


def repo_revision():
    """ 代码仓回退到指定版本 """
    pass


def repo_run_test():
    """ 执行单元测试 """
    local("{0} {1} unittest".format(local_python_exec, local_manager_script))
