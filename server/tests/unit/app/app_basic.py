# encoding: utf-8

"""
twinado server.tests.unit.application.app_basic

~~~~~~

twinado server application 功能单元测试模块的 app 核心功能测试

"""

from tornado.testing import gen_test

from server.tests.unit import ServerTestBase
from server.application import create_app

from server.tests.unit.app.handlers.main import HomePageHandler


class AppTest(ServerTestBase):
    def get_app(self):
        app = create_app(handlers=[('/', HomePageHandler)], mode='testing')
        return app

    @gen_test
    def test_app_can_start(self):
        home_page_url = self.get_url('/')
        response = yield self.client.fetch(home_page_url)
        self.assertIn(b'home page', response.body)
