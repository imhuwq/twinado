# encoding: utf-8

"""
twinado deploy.tasks.supervisor

~~~~~~

twinado 部署流程中 supervisor 环境相关的 task

"""

from fabric.api import run, abort, put
from fabric.contrib.files import exists

from deploy.config import *


def supervisorctl(cmd):
    return run("{0} {1} -c {2} {3}".format(supervisor_env,
                                           supervisorctl_exec,
                                           supervisor_conf,
                                           cmd))


def supervisor_prepare():
    """ 安装, 配置并启动 supervisor 服务"""
    supervisor_install()
    supervisor_config()
    supervisor_start()


def supervisor_install():
    """ 安装 supervisor  """
    run("{0} install supervisor".format(pip2_exec))


def supervisor_config():
    """ 配置 supervisor """
    if not exists(config_path):
        run("mkdir -p {0}".format(config_path))
    put(local_supervisor_config, supervisor_conf)


def supervisor_start():
    """ 开启 supervisor 服务 """
    if not exists(supervisor_log):
        run("mkdir -p {0} && touch {1}".format(log_path, supervisor_log))

    if not exists(supervisor_pid):
        run("mkdir -p {0} && touch {1}".format(run_path, supervisor_pid))

    supervisor_shutdown()

    run("{0} {1} -c {2}".format(supervisor_env,
                                supervisord_exec,
                                supervisor_conf))


def supervisor_shutdown():
    """ 关闭 supervisor 自己 """
    supervisorctl("shutdown")
