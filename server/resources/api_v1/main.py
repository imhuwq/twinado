# encoding: utf-8

"""
twinado server.resource.api_v1.main

~~~~~~

api_v1.main: api v1 的共性业务

api: host/api/v1/main
-------------------------------------------------------------
/                                       index
-------------------------------------------------------------
/index                                  index
-------------------------------------------------------------
/xsrf                                   获取 xsrf token
-------------------------------------------------------------

"""

from server.application.tornado_handler import BaseHandler
from server.resources.api_v1 import apiv1

main = apiv1.create_resource('main', prefix='/main')


@main.route(r'/')
class HomePage(BaseHandler):
    def get(self, *args, **kwargs):
        return self.write('home page')


@main.route(r'/index')
class IndexPage(BaseHandler):
    def get(self):
        return self.redirect(self.reverse_url('api_v1.main.HomePage'))


@main.route(r'/xsrf')
class XsrfToken(BaseHandler):
    def get(self):
        token = self.xsrf_token
        token = token.decode()
        return self.write({'token': token})
