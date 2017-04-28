# encoding: utf-8

"""
twinado server.tests.unit.model.user

~~~~~~

twinado server 单元测试模块的 user model 测试

"""

import datetime

from sqlalchemy.exc import IntegrityError

from server.application import db
from server.models import User
from server.tests.unit import ApplicationTestBase


class UserModelTest(ApplicationTestBase):
    def test_user_create(self):
        user = User(name="john")
        db.session.add(user)
        db.session.commit()

        created = db.session.query(User).get(1)
        self.assertTrue(created is not None)
        self.assertTrue(created.name == "john")
        self.assertTrue(created.uuid is not None)
        self.assertTrue(created == db.session.query(User).filter_by(name="john").first())

    def test_user_password(self):
        user = User(name="john", email="john@hu.com")
        password = "apasswordshouldbeinvisible"
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        created = db.session.query(User).get(1)
        self.assertTrue(created.authenticate(password))
        self.assertFalse(created.authenticate("adf2434gdsfsfs"))

    def test_user_name_email_unique(self):
        user = User(name="john", email="john@hu.com")
        password = "apasswordshouldbeinvisible"
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        with self.assertRaises(IntegrityError):
            user = User(name="john", email="john@huhuhu.com")
            password = "apasswordshouldbeinvisible"
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

        db.session.rollback()

        with self.assertRaises(IntegrityError):
            user = User(name="johasdn", email="john@hu.com")
            password = "apasswordshouldbeinvisible"
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

    def test_user_auth_token(self):
        user = User(name="john", email="john@hu.com")
        token = user.gen_auth_token()
        db.session.commit()
        self.assertTrue(user.validate_auth_token(token))
        timedelta = datetime.timedelta(minutes=22)
        self.assertFalse(user.validate_auth_token(token, timedelta))
