# encoding: utf-8

"""
twinado server.extensions.database

~~~~~~

基于 sqlalchemy 的数据库插件

    Database 类用于对 sqlalchemy 的 session 管理和对 sqlalchemy models 的 query
    Model 用于 sqlalchemy orm model 的基类
    Model 已经被设置成 Database 实例的属性, 所以拿到 database 实例后用 database 实例去实现 orm model 即可

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base


class DataBaseURIError(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


Model = declarative_base()


class DataBase:
    def __init__(self, app=None):
        self.app = app
        self.engine = None
        self.session = None
        self.query = None
        self.Model = Model

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.db_uri = app.settings.get("database_uri", None)

        if app.db_uri is None:
            raise DataBaseURIError("Please specify your database URI")

        self.engine = create_engine(app.db_uri)
        self.session = scoped_session(sessionmaker(bind=self.engine))
        self.query = self.session.query

        app.db = self

    def create_all(self):
        self.Model.metadata.create_all(self.engine)

    def drop_all(self):
        self.Model.metadata.drop_all(self.engine)
