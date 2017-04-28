# encoding: utf-8

"""
twinado deploy.tasks.nginx

~~~~~~

twinado 部署流程中 nginx 相关的 task

"""

from fabric.api import sudo

from deploy.tasks.apt import apt_update


def nginx_prepare():
    """ 安装, 配置和启动 nginx """
    nginx_install()
    nginx_restart()


def nginx_install():
    """ 安装 nginx"""
    apt_update()
    sudo("apt-get install nginx")


def nginx_status():
    """ 获取 nginx status """
    sudo("service nginx status")


def nginx_start():
    """ 开启 nginx 服务"""
    sudo("service nginx start")


def nginx_stop():
    """ 停止 nginx 服务 """
    sudo("service nginx stop")


def nginx_restart():
    """ 重启 nginx 服务"""
    nginx_stop()
    nginx_start()


def nginx_reload():
    """ 软重启 nginx """
    sudo("nginx -s reload")
