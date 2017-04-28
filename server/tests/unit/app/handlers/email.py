from server.application.tornado_handler import BaseHandler

from . import test

email = test.create_resource('email', prefix='/email')


@email.route('/send')
class SendEmail(BaseHandler):
    def get(self):
        self.send_email('56473348@qq.com', 'test send_email', 'hello world')
        self.response.update({'status': 1, 'msg': 'email sent'})
        return self.write(self.response)
