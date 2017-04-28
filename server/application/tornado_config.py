import os

from copy import deepcopy

PERMITTED_MODES = ["production", "development", "testing"]


class ConfigMeta(type):
    def __new__(cls, cls_name, cls_bases, cls_dict):
        config_template = {}

        cls_dict_copy = deepcopy(cls_dict)
        for key, value in cls_dict_copy.items():
            if not key.startswith("_"):
                cls_dict.pop(key)
                config_template[key] = deepcopy(value)
        cls_dict["_configs"] = config_template

        return type.__new__(cls, cls_name, cls_bases, cls_dict)


class Config(metaclass=ConfigMeta):
    _configs = None  # all configs below are gathered here by ConfigMeta at the class creation time

    instance_dir = os.path.abspath(os.path.dirname(__file__))
    server_dir = os.path.abspath(os.path.join(instance_dir, "../"))
    repo_dir = os.path.abspath(os.path.join(server_dir, "../"))

    cookie_secret = ")5T1~dLb~isIUrta2&_Cu90xzKmx!V6T2A^eI~z#33ZlPTm6SaFo(IUSBVU6"
    debug = False
    xsrf_cookies = True

    email_config = {
        "host": "",
        "port": 465,
        "user": "",
        "password": ""
    }

    database_config = {
        "username": "twinado",
        "password": "twinado",
        "database": "twinado",
        "host": "a-sz-s-6",
    }

    database_uri = "postgresql+psycopg2://%s:%s@%s/%s" % (database_config.get("username"),
                                                          database_config.get("password"),
                                                          database_config.get("host"),
                                                          database_config.get("database"))

    redis_config = {
        "host": "a-sz-s-6",
        "port": 6379,
        "db": 5
    }

    realicloud_config = {
        "host": "http://staging.realicloud.realibox.com",
        "app_token": "4c4fa8eaa83c1abbbfa029cf2c76299bc1bd41e7",
        "calib_feature_token": "83f262dfcfab30f69107efd926dda41f558db1b6",
        "calib_api": "/api/v1/jobs",
        "calib_callback": "api_v1.photo.PhotoInfo"
    }

    def __init__(self, mode=None):

        if mode not in PERMITTED_MODES:
            raise AttributeError("mode %s is not in %s." % (mode, PERMITTED_MODES))

        self.mode = mode
        self.configs = deepcopy(Config._configs)
        self.configs["app_mode"] = mode

        if mode == "development":
            self.configs["database_uri"] = "sqlite:///" + os.path.join(self.configs["repo_dir"], "deve.sqlite")
            self.configs["debug"] = True
        elif mode == "testing":
            self.configs["database_uri"] = "sqlite:///" + os.path.join(self.configs["repo_dir"], "test.sqlite")
            self.configs["debug"] = True
            self.configs["xsrf_cookies"] = False
