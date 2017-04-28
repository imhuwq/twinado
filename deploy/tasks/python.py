# encoding: utf-8

"""
twinado deploy.tasks.python

~~~~~~

twinado 部署流程中准备 python 环境相关的 task

"""

from fabric.api import run
from fabric.contrib.files import exists

from deploy.config import *
from deploy.tasks.git import git_prepare


def python_prepare():
    """ 安装和配置 python 的虚拟环境 """
    python_install_pyenv()
    python_install_python()
    python_install_python2()
    python_setup_douban_mirror()
    python_install_virtual_env()


def python_install_pyenv():
    """ 安装 pyenv """
    git_prepare()

    if not exists(pyenv_path):
        run("git clone {0} {1}".format(pyenv_git_repo, pyenv_path))

    if not exists(pyenv_plugin_venv_path):
        run("git clone {0} {1}".format(pyenv_plugin_venv_repo, pyenv_plugin_venv_path))


def python_install_python():
    """ 使用 pyenv 安装 python3 """
    if not exists(python_base_path):
        if exists(python_cache_file):
            run("rm {0}".format(python_cache_file))
        run("mkdir -p {0}".format(python_cache_dir))
        run("wget {0} -q -P {1}".format(python_mirror_uri, python_cache_dir))
        run("export PYTHON_BUILD_CACHE_PATH={0} && {1} install {2}".format(python_cache_dir, pyenv_exec_path,
                                                                           python_version))


def python_install_python2():
    """ 使用 pyenv 安装 python2 """
    if not exists(python2_base_path):
        if exists(python2_cache_file):
            run("rm {0}".format(python2_cache_file))
        run("mkdir -p {0}".format(python2_cache_dir))
        run("wget {0} -q -P {1}".format(python2_mirror_uri, python2_cache_dir))
        run("export PYTHON_BUILD_CACHE_PATH={0} && {1} install {2}".format(python2_cache_dir, pyenv_exec_path,
                                                                           python2_version))


def python_setup_douban_mirror():
    """ 设置使用 douban 的 pip 镜像 """
    run("mkdir -p {0}".format(pip_conf_dir))
    if not exists(pip_conf_file):
        run("touch {0}".format(pip_conf_file))
        run("echo [global] >> {0}".format(pip_conf_file))
        run("echo index-url = https://pypi.doubanio.com/simple >> {0}".format(pip_conf_file))


def python_install_virtual_env():
    """ 安装 python 虚拟环境 """
    if not exists(python_path):
        run("{0} virtualenv {1} {2}".format(pyenv_exec_path, python_version, application))
    if not exists(python2_path):
        run("{0} virtualenv {1} {2}-py2".format(pyenv_exec_path, python2_version, application))


def python_install_requirements():
    """ 安装 python 所有依赖包 """
    if exists(application_pip_req):
        run("{0} install -r {1} --upgrade".format(pip_exec, application_pip_req))
