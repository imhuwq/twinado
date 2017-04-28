# encoding: utf-8

"""
twinado server.tests.unit.application.api

~~~~~~

twinado server application 功能单元测试模块的 api 功能测试

"""

from tornado.testing import gen_test

from server.tests.unit import ServerTestBase


class APITest(ServerTestBase):
    def test_01_reverse_url(self):
        user_login_path = self.app.reverse_url('test.user.UserLogin')
        self.assertEqual(user_login_path, '/test/v1/user/login')

    @gen_test
    def test_02_reverse_url_with_args(self):
        fans_of_city = self.app.reverse_url('test.user.FansOfCity', 'guangzhou')
        self.assertEqual(fans_of_city, '/test/v1/user/guangzhou/fans')

        url = self.reverse_url('test.user.FansOfCity', 'guangzhou')
        response = yield self.client.fetch(url)
        response = response.body.decode()
        self.assertEqual(response, 'guangzhou')
