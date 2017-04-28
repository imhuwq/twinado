# encoding: utf-8

"""
twinado server.extensions.redis

~~~~~~

基于 tornadis 的 redis client 插件, 异步的

"""

import tornadis


class Redis:
    def __init__(self, app=None):
        self.client = None
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        redis_config = app.settings.get("redis_config")
        host = redis_config.get('host') or 'localhost'
        port = redis_config.get('port') or 6379
        db = redis_config.get('db') or 1
        self.client = tornadis.Client(host=host, port=port, db=db, autoconnect=True)

        app.redis = self
