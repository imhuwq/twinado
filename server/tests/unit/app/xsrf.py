# encoding: utf-8

"""
twinado server.tests.unit.application.xsrf

~~~~~~

twinado server application 功能单元测试模块的 xsrf 功能测试

"""

import json
from urllib.parse import urlencode

from tornado.httpclient import HTTPRequest, HTTPError
from tornado.testing import gen_test

from server.application import create_app
from server.resources.api_v1 import apiv1
from server.tests.unit import ServerTestBase
from server.tests.unit.app.handlers import test


class XSRFTest(ServerTestBase):
    def setUp(self):
        super(XSRFTest, self).setUp()
        self.target = self.reverse_url('test.xsrf.XsrfToken')

    def get_app(self):
        handlers = apiv1.handlers + test.handlers
        app = create_app(handlers, mode='development')
        return app

    @gen_test
    def test_01_get_xsrf(self):
        response = yield self.client.fetch(self.target)
        self.assertTrue(response.code == 200)
        self.assertTrue(response.body != b'')

    @gen_test
    def test_02_post_with_xsrf(self):
        response = yield self.client.fetch(self.target)
        response = json.loads(response.body.decode())
        xsrf = response.get('xsrf')

        body = {'_xsrf': xsrf}
        body = urlencode(body)

        headers = {'Cookie': '_xsrf=%s' % xsrf}
        request = HTTPRequest(url=self.target, method='POST', headers=headers, body=body)
        response = yield self.client.fetch(request)
        self.assertTrue(response.code == 200)

        response = response.body.decode()
        response = json.loads(response)
        body = response.get('msg')
        self.assertTrue(body == 'ok')

    @gen_test
    def test_03_post_without_xsrf(self):
        body = {}
        body = urlencode(body)
        request = HTTPRequest(url=self.target, method='POST', body=body)

        with self.assertRaises(HTTPError):
            yield self.client.fetch(request)
