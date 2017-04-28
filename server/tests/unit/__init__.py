# encoding: utf-8

"""
twinado server.tests.unit

~~~~~~

twinado server 的单元测试模块

架构如下:
    unit.app: 基础功能测试
    unit.extension: 插件测试
    unit.model: 数据库 model 测试
    unit.util: utils 各函数与类的测试
"""

from unittest import TestCase

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase


class UtilTestBase(TestCase):
    def __init__(self, *args, **kwargs):
        super(UtilTestBase, self).__init__(*args, **kwargs)


class ApplicationTestBase(AsyncHTTPTestCase):
    def __init__(self, *args, **kwargs):
        super(ApplicationTestBase, self).__init__(*args, **kwargs)
        self.app = None

    def get_app(self):
        return create_app((), mode='testing')

    def reverse_url(self, name, *args, **kwargs):
        path = self.app.reverse_url(name, *args, **kwargs)
        return self.get_url(path)

    def get_new_ioloop(self):  # must have
        return IOLoop.instance()

    def setUp(self):
        super(ApplicationTestBase, self).setUp()
        self.app = self.get_app()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        super(ApplicationTestBase, self).tearDown()


class ServerTestBase(ApplicationTestBase):
    def __init__(self, *args, **kwargs):
        super(ServerTestBase, self).__init__(*args, **kwargs)
        self.client = None

    def get_app(self):
        handlers = test.handlers
        return create_app(handlers, mode='testing')

    def setUp(self):
        super(ServerTestBase, self).setUp()

        self.client = AsyncHTTPClient(self.io_loop)

        user = User(name='john', email='john@hu.com', uuid='12345')
        password = 'cat2dog'
        user.set_password(password)
        db.session.add(user)
        db.session.commit()


from server.tests.unit.app import *
from server.tests.unit.model import *
from server.tests.unit.util import *
from server.tests.unit.extension import *
