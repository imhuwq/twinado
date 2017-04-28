# encoding: utf-8

"""
twinado server.extension

~~~~~~

依赖于 tornado app 而运行的功能插件

架构如下:
    extension.database: sqlalchemy 数据库插件
    extension.redis: tornadis redis 插件
    extension.session: 基于 redis 的 session 插件
    extension.email: 邮件插件

"""

from server.extensions.database import DataBase
from server.extensions.redis import Redis
from server.extensions.session import Session
from server.extensions.email import Email
