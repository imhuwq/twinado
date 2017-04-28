# encoding: utf-8

"""
twinado deploy.utils.task

~~~~~~

twinado 部署流程中的 task 管理

"""

from collections import OrderedDict
from functools import wraps

from fabric.api import env

from deploy.utils.console import notify, colorize, ConsoleColor, init, good, fail

DeployError = type("DeployError", (Exception,), {})

TaskRegistrationError = type("TaskRegistrationError", (Exception,), {})
TaskNotFound = type("TaskNotFound", (Exception,), {})


class TaskManager:
    """ Task Manager
     通过类方法来串联子任务, 根据 role 和 stage 来设置全局环境
     """

    def __init__(self, name="task"):
        self.name = name
        self.tasks = []
        self._task_map = OrderedDict()

    def register(self, func):
        task_name = func.__name__

        @wraps(func)
        def func_with_notify():
            msg = "%s: %s on role:%s at stage:%s..." % (self.name, colorize(task_name, ConsoleColor.ORANGE),
                                                        colorize(env.role, ConsoleColor.ORANGE),
                                                        colorize(env.stage.name, ConsoleColor.ORANGE))

            notify(init, msg)
            status = True
            exec = None
            try:
                rv = func()
            except Exception as e:
                exec = e
                status = False
            else:
                return rv
            finally:
                if status is False:
                    notify(fail, msg)
                    raise exec
                else:
                    notify(good, msg)

        if task_name in self.tasks:
            raise TaskRegistrationError("%s is already registered")
        else:
            self.tasks.append(task_name)
            self._task_map[task_name] = func_with_notify

    def confirm(self, task_name):
        if task_name == "all":
            task_name = self.tasks[:]
        else:
            if task_name not in self.tasks:
                raise TaskNotFound("{0} is not a registered task".format(task_name))
            task_name = [task_name]

        return task_name

    def retrieve(self, task_name):
        return self._task_map.get(task_name)

    @staticmethod
    def setup_env(role, stage):
        env.abort_exception = DeployError

        if stage.key_filename:
            env.key_filename = stage.key_filename

        if stage.use_ssh_config:
            env.use_ssh_config = True
        env.host_string = stage.host
        env.port = stage.port
        env.user = stage.user
        env.password = stage.password

        env.stage = stage
        env.role = role

    def run_all(self):
        for task_name, task_func in self._task_map.items():
            task_func()
