# encoding: utf-8

"""
twinado deploy.tasks.git

~~~~~~

twinado 部署流程中 git 相关的 task

"""

from fabric.contrib.files import exists
from fabric.api import run, sudo

from deploy.tasks.apt import require_apt_update


def git_prepare():
    """ 准备 git """
    install_git()


def install_git():
    """ 安装 git """
    if not exists("/usr/bin/git"):
        sudo("apt-get install git")
