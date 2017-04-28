# encoding: utf-8

"""
twinado deploy.tasks.files

~~~~~~

twinado 部署流程中 apt 相关的 task

"""

from functools import wraps

from fabric.api import runs_once, sudo


@runs_once
def apt_update():
    """ 更新 apt 源 """
    sudo("apt-get update")


def require_apt_update(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        apt_update()
        return func(*args, **kwargs)

    return wrapper
