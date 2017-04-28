# encoding: utf-8

"""
twinado deploy.config

~~~~~~

twinado 部署时会用到的各种变量

"""

import os

from deploy.utils import Stage

# 项目路径
project_path = "~/twinado"

shared_path = "{0}/shared".format(project_path)
config_path = "{0}/config".format(shared_path)
log_path = "{0}/log".format(shared_path)
run_path = "{0}/run".format(shared_path)

# application
application = "twinado"
application_port = [8000, 8001]
application_repo = "git@gitlab.shinemi.cn:twinado/twinado.git"
application_path = "{0}/twinado-server".format(project_path)
application_conf = "{0}/tornado_config.py".format(config_path)
application_conf_link = "{0}/server/instance/tornado_config.py".format(application_path)
application_pip_req = "{0}/requirements.txt".format(application_path)

# pyenv
pyenv_path = "~/.pyenv"
pyenv_git_repo = "http://gitlab.shinemi.cn/mirrors/pyenv.git"
pyenv_exec_path = "{0}/bin/pyenv".format(pyenv_path)
pyenv_plugin_venv_repo = "http://gitlab.shinemi.cn/mirrors/pyenv-virtualenv.git"
pyenv_plugin_venv_path = "{0}/plugins/pyenv-virtualenv".format(pyenv_path)

# python
python_version = "3.5.2"
python_mirror_host = "http://mirrors.sohu.com/python"
python_mirror_uri = "{0}/{1}/Python-{2}.tar.xz".format(python_mirror_host, python_version, python_version)
python_cache_dir = "~/cache"
python_cache_file = "{0}/Python-{1}.tar.xz".format(python_cache_dir, python_version)

python_base_path = "{0}/versions/{1}".format(pyenv_path, python_version)
python_path = "{0}/versions/{1}".format(pyenv_path, application)
python_exec = "{0}/bin/python".format(python_path)
pip_exec = "{0}/bin/pip".format(python_path)
alembic_exec = "{0}/bin/alembic".format(python_path)

# python2
python2_version = "2.7.12"
python2_mirror_uri = "{0}/{1}/Python-{2}.tar.xz".format(python_mirror_host, python2_version, python2_version)
python2_cache_dir = "~/cache"
python2_cache_file = "{0}/Python-{1}.tar.xz".format(python_cache_dir, python2_version)

python2_base_path = "{0}/versions/{1}".format(pyenv_path, python2_version)
python2_path = "{0}/versions/{1}-py2".format(pyenv_path, application)
python2_exec = "{0}/bin/python".format(python2_path)
pip2_exec = "{0}/bin/pip".format(python2_path)

# pip
pip_conf_dir = "~/.pip"
pip_conf_file = "{0}/pip.conf".format(pip_conf_dir)

# supervisor
supervisor_conf = "{0}/supervisor.conf".format(config_path)
supervisor_log = "{0}/supervisord.log".format(log_path)
supervisor_pid = "{0}/supervisord.pid".format(run_path)
supervisord_exec = "{0}/bin/supervisord".format(python2_path)
supervisorctl_exec = "{0}/bin/supervisorctl".format(python2_path)
supervisor_env = "export PYTHON_PATH={0}; " \
                 "export APP_PATH={1}; " \
                 "export SHARED_PATH={2} " \
                 "export APP_LOG_PREFIX={3} && ".format(python_exec,
                                                        application_path,
                                                        shared_path,
                                                        application)
# 本地相关
local_deploy_dir = os.path.abspath(os.path.dirname(__file__))
local_shared_dir = os.path.join(local_deploy_dir, "shared")
local_config_dir = os.path.join(local_shared_dir, "config")
local_supervisor_config = os.path.join(local_config_dir, "supervisor.conf")
local_application_config = os.path.join(local_config_dir, "tornado_config.py")

local_repo_dir = os.path.dirname(local_deploy_dir)
local_python_exec = "~/.pyenv/versions/twinado/bin/python"
local_manager_script = "{0}/manager.py".format(local_repo_dir)

local_stage = Stage(name="local",
                    branch="developer",
                    host="127.0.0.1",
                    port=22,
                    user="deploy",
                    password="..admin123",
                    use_ssh_config=True)

staging_stage = Stage(name="staging",
                      branch="staging",
                      host="a-sz-s-13.op.shinemi.cn",
                      port=2213,
                      user="deploy",
                      password="deploy11235813",
                      key_filename="~/.ssh/aly-staging",
                      use_ssh_config=True)
