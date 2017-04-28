# encoding: utf-8

"""
twinado server.models.user

~~~~~~

twinado server 的 user orm

user 表
-------------------------------------------------------------------------------------------------------------
id                          integer                     用户 id, primary
-------------------------------------------------------------------------------------------------------------
uuid                        string                      用户 uuid, 必须, 用户的唯一标志
-------------------------------------------------------------------------------------------------------------
name                        string                      用户昵称, 唯一
-------------------------------------------------------------------------------------------------------------
email                       string                      用户邮箱, 用于登录
-------------------------------------------------------------------------------------------------------------
password                    string                      用户密码, 用于登录, 私有属性
-------------------------------------------------------------------------------------------------------------
auth token                  string                      用户 auth token, 用于重置密码, 私有熟悉
-------------------------------------------------------------------------------------------------------------
auth token datetime         datetime                    用户 auth token 的生成日期, 用户验证 auth token 的有效期
-------------------------------------------------------------------------------------------------------------

"""

import datetime
import re
from random import SystemRandom
from string import ascii_letters, digits

from bcrypt import hashpw, checkpw, gensalt
from sqlalchemy import Column, String, Integer, DateTime

from server.application import db
from server.utils import gen_uuid

UserModelError = type("UserModelError", (Exception,), {})


class User(db.Model):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    uuid = Column("uuid", String, nullable=False, unique=True, default=gen_uuid)

    name = Column("name", String, unique=True)
    email = Column("email", String, unique=True)
    __password = Column("password", String)

    __auth_token = Column("auth_token", String)
    __auth_token_datetime = Column("auth_token_datetime", DateTime)

    def set_password(self, value):
        if not isinstance(value, bytes):
            value = value.encode()
        self.__password = hashpw(value, gensalt())

    def authenticate(self, password):
        if not isinstance(password, bytes):
            password = password.encode()
        return checkpw(password, self.__password)

    @staticmethod
    def validate_name(name):
        chars = ascii_letters + digits + "._"
        chars_length = 0

        for text in name:
            if "\u4e00" <= text <= "\u9fff":
                chars_length += 2
            elif text in chars:
                chars_length += 1
            else:
                return False
        if chars_length <= 2 or chars_length >= 21:
            return False

        return True

    @staticmethod
    def validate_email(email):
        email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+$")
        return email_pattern.match(email) is not None

    @staticmethod
    def gen_random_password():
        chars = ascii_letters + digits
        codes = [SystemRandom().choice(chars) for _ in range(10)]
        password = "".join(codes)
        return password

    def gen_auth_token(self):
        chars = ascii_letters + digits
        codes = [SystemRandom().choice(chars) for _ in range(24)]
        token = "".join(codes)
        self.__auth_token = token
        self.__auth_token_datetime = datetime.datetime.utcnow()
        db.session.flush()
        return token

    def validate_auth_token(self, token, timedelta=None):
        if token == self.__auth_token:
            if timedelta is None:
                auth_generated_time = self.__auth_token_datetime
                current_time = datetime.datetime.utcnow()
                timedelta = current_time - auth_generated_time

            return timedelta < datetime.timedelta(minutes=20)

        return False

    @staticmethod
    def validate_password(password):
        if len(password) < 7:
            return False

        letter_pattern = re.compile(r"([a-zA-Z])")
        if not letter_pattern.findall(password):
            return False

        digit_pattern = re.compile(r"(\d)")
        if not digit_pattern.findall(password):
            return False

        return True
