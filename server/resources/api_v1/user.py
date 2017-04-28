# encoding: utf-8

"""
twinado server.resource.api_v1.user

~~~~~~

api_v1.main: api v1 的 user 相关业务

api: host/api/v1/users
-------------------------------------------------------------
/                                       获取当前用户消息简报
-------------------------------------------------------------
/<user_uuid>/profile/                   获取当前用户的详细信息
-------------------------------------------------------------
/login                                  用户登录
-------------------------------------------------------------
/logout                                 用户注销
-------------------------------------------------------------
/register                               用户注册
-------------------------------------------------------------
/<user_uuid>/password                   未登录用户重置密码
-------------------------------------------------------------
/<user_uuid>/password/change            已登录用户更改用户密码
-------------------------------------------------------------

"""

from itertools import compress
from tornado.gen import coroutine

from server.models import User
from server.utils import gen_uuid
from server.application.tornado_handler import Argument
from server.application.tornado_handler import BaseHandler
from server.application.tornado_handler import login_required

from server.resources.api_v1 import apiv1

user = apiv1.create_resource("user", prefix="/users")


# get current user info
@user.route("/")
class UserIndex(BaseHandler):
    def get(self):
        if self.current_user:
            info = {"name": self.current_user.name,
                    "email": self.current_user.email,
                    "uuid": self.current_user.uuid,
                    "isAnonymous": False}
        else:
            info = {"name": "anonymousUser",
                    "email": "anonymouse@example.com",
                    "uuid": gen_uuid(),
                    "isAnonymous": True}
        self.start_response(**info)


# get specified user profile
@user.route("/<user_uuid>/profile/")
class UserProfile(BaseHandler):
    def get(self, user_uuid):
        user_ = self.db.query(User).filter_by(uuid=user_uuid).first()
        if user_ is not None:
            info = {"name": user_.name,
                    "email": user_.email,
                    "uuid": user_.uuid}
            self.start_response(**info)
        else:
            self.raise_error(404, -1, "user does not exist")


# user login
@user.route("/login")
class UserLogin(BaseHandler):
    @coroutine
    def post(self):
        if self.current_user:
            self.start_response(status=0, msg="user is already logged in")
        else:
            email, password = self.parse_arguments([Argument("email"), Argument("password")])
            logging_user = self.db.query(User).filter_by(email=email).first()
            if logging_user and logging_user.authenticate(password):
                yield self.login(logging_user)
                self.start_response(status=1, msg="login success")
            else:
                self.raise_error(400, msg="invalid email or password")


# user logout
@user.route("/logout")
class UserLogout(BaseHandler):
    def post(self):
        if self.current_user:
            self.logout()
            self.start_response(msg="logout success")
        else:
            self.start_response(status=0, msg="user is not logged in")


# user register
@user.route("/register")
class UserRegister(BaseHandler):
    @coroutine
    def post(self):
        if self.current_user:
            self.start_response(status=0, msg="user is logged in")
        else:
            name, email, password = self.parse_arguments([Argument("name"),
                                                          Argument("email"),
                                                          Argument("password")])

            name_is_valid = User.validate_name(name)
            email_is_valid = User.validate_email(email)
            password_is_valid = User.validate_password(password)
            validate_info = [name_is_valid, email_is_valid, password_is_valid]

            if not all(validate_info):
                invalid = ["name", "email", "password"]
                invalid = list(compress(invalid, validate_info))
                self.raise_error(400, msg="invalid user info", invalid=invalid)
            else:
                existed_user = self.db.query(User).filter((User.name == name) | (User.email == email)).first()
                if existed_user:
                    in_use = ["email", "name"]
                    in_use_info = [existed_user.email == email, existed_user.name == name]
                    in_use = list(compress(in_use, in_use_info))
                    self.raise_error(400, msg="user info is in use", in_use=in_use)
                else:
                    new_user = User(name=name, email=email)
                    new_user.set_password(password)
                    self.db.session.add(new_user)
                    self.db.session.commit()
                    info = {"password": password, "name": name, "email": email}
                    yield self.login(new_user)
                    self.start_response(**info)


# change user password
@user.route("/<user_uuid>/password/change")
class UserChangePassword(BaseHandler):
    @login_required
    def post(self, user_uuid):
        (password, new_password) = self.parse_arguments([Argument("password"),
                                                         Argument("new_password")])
        if not self.current_user.authenticate(password):
            self.raise_error(400, msg="current password is incorrect")
        else:
            if not User.validate_password(new_password):
                self.raise_error(400, msg="password is not secure enough")
            else:
                self.current_user.set_password(new_password)
                self.db_session.commit()
                self.start_response(msg="password updated successfully")


# user forget password
@user.route("/<user_uuid>/password")
class UserForgetPassword(BaseHandler):
    def get(self, user_uuid):
        existed_user = self.db.query(User).filter_by(uuid=user_uuid).first()
        if existed_user is not None:
            auth_token = existed_user.gen_auth_token()
            email = existed_user.email

            email_content = "Someone reports that you have forgotten your password. " \
                            "Click the following link to reset your password:" \
                            " {0}?email={1}&token={2}." \
                            "Or you can ignore this message if that is not initiated by you". \
                format(self.reverse_url("api_v1.user.UserForgetPassword", user_uuid), email, auth_token)

            self.send_email(receiver=email, subject="Reset Password", content=email_content)

            self.start_response(
                msg="an instruction about resetting password has been sent to your email, "
                    "please check your inbox.")
        else:
            self.raise_error(404, "invalid email address")

    def post(self, user_uuid):
        existed_user = self.db.query(User).filter_by(uuid=user_uuid).first()
        if existed_user:
            token, password = self.parse_arguments([Argument("token"),
                                                    Argument("password")])
            if existed_user.validate_auth_token(token):
                if User.validate_password(password):
                    existed_user.set_password(password)
                    existed_user.gen_auth_token()
                    self.start_response(msg="password has been reset successfully")
                else:
                    self.raise_error(403, msg="new password is illegal, perhaps not secure enough")
            else:
                self.raise_error(400, msg="invalid token")
        self.raise_error(404, msg="user does not exist")
