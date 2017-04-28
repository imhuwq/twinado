from server.application.tornado_handler import BaseHandler

from . import test

xsrf = test.create_resource('xsrf', prefix='/xsrf')


@xsrf.route('/')
class XsrfToken(BaseHandler):
    def get(self):
        xsrf = self.xsrf_token
        xsrf = xsrf.decode()
        return self.write({'xsrf': xsrf})

    def post(self):
        return self.write({'msg': 'ok'})
