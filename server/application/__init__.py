# encoding: utf-8

"""
twinado server.application

~~~~~~

对 tornado web application 的定制

架构如下:
    application.tornado_app: tornado web application 的定制
    application.tornado_api: 实现装饰器模式的路由
    application.tornado_handler: tornado request handler 的定制
    application.tornado_config: tornado web server 配置文件模板

"""

from server.application.tornado_app import Application
from server.application.tornado_api import API

from server.extensions.database import DataBase
from server.extensions.redis import Redis
from server.extensions.email import Email

from server.instance import Config

redis = Redis()
db = DataBase()
email = Email()


def create_app(handlers, mode="production"):
    config = Config(mode)

    app = Application(
        handlers=handlers,
        **config.configs
    )

    db.init_app(app)
    redis.init_app(app)
    email.init_app(app)

    if mode != "production":
        db.create_all()
    return app
