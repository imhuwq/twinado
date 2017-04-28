# encoding: utf-8

"""
twinado deploy.utils.stage

~~~~~~

twinado 部署 stage 管理

stage 一般用来指示服务器的状态, 比如 production, development, test 等

"""

StageRegistrationError = type("StageRegistrationError", (Exception,), {})
StageNotFound = type("StageNotFound", (Exception,), {})


class Stage:
    def __init__(self, name, branch, host, port=22,
                 user="deploy", password=None,
                 key_filename=None, use_ssh_config=False):
        self.name = name
        self.branch = branch
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.key_filename = key_filename
        self.use_ssh_config = use_ssh_config

        StageManager.register(self)

    def __repr__(self):
        return self.name


class StageManager:
    STAGES = []
    _stage_obj_map = {}

    @classmethod
    def register(cls, stage):
        if stage.name in cls.STAGES:
            raise StageRegistrationError("{0} is already registered".format(stage.name))

        cls.STAGES.append(stage.name)
        cls._stage_obj_map[stage.name] = stage

    @classmethod
    def confirm(cls, stage_name):
        if stage_name not in cls.STAGES:
            raise StageNotFound("{0} is not a registered stage".format(stage_name))
        return True

    @classmethod
    def retrieve(cls, stage_name):
        cls.confirm(stage_name)
        return cls._stage_obj_map.get(stage_name)
