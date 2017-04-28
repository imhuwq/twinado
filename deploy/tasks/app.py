# encoding: utf-8

"""
twinado deploy.tasks.files

~~~~~~

twinado 部署流程中 app 相关的 task

"""

from deploy.tasks.supervisor import supervisorctl


def app_status():
    """ 获取 app status"""
    supervisorctl("status twinado-8000")
    supervisorctl("status twinado-8001")


def app_start():
    """ 开启 app """
    supervisorctl("start twinado-8000")
    supervisorctl("start twinado-8001")


def app_stop():
    """ 停止 app """
    supervisorctl("stop twinado-8000")
    supervisorctl("stop twinado-8001")


def app_restart():
    """ 重启 app """
    app_stop()
    app_start()
