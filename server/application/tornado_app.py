# encoding: utf-8

"""
twinado server.application.tornado_app

~~~~~~

对 tornado web application 的定制

"""

from tornado.web import Application as BaseApplication


class Application(BaseApplication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.db = None
        # self.db_uri = db_uri
        # self.redis = None

        self.mode = 'production'
