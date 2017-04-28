from server.application.tornado_handler import BaseHandler


class HomePageHandler(BaseHandler):
    def get(self):
        return self.write('home page')
