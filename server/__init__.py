# encoding: utf-8

"""
twinado server

~~~~~~

twinado 的 web 服务端服务端, 基于 tornado + sqlalchemy + redis

架构如下:
    server.application: 对 tornado 的定制
    server.extensions: 依赖于 tornado app 而运行的功能插件, 比如 邮件
    server.models: web 数据库 models
    server.modules: 独立于 tornado app 而运行的模块, 比如 celery 等
    server.utils: 通用性的一些函数/类
    server.tests: 单元测试和 api 测试

    server.resource: web api 业务

    server.instance: 服务器的配置文件

"""
