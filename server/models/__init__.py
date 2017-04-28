# encoding: utf-8

"""
twinado server.models

~~~~~~

twinado server 的数据库设计

架构如下:
    models.migrations: 数据库迁移脚本, 由 alembic 自动生成并管理
    models.user: user 数据库设计

"""

from server.models.user import User

# the next line must be kept for alembic revision to work
from server.extensions.database import Model
