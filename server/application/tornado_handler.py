# encoding: utf-8

"""
twinado server.application.tornado_handler

~~~~~~

tornado web request handler 的定制

"""

import uuid
import json

from functools import wraps

from tornado.gen import coroutine
from tornado.web import RequestHandler, Finish
from tornado.websocket import WebSocketHandler

from server.models import User

from server.extensions import Session
from server.extensions import Email

from server.utils import silent_return_none


class Argument:
    def __init__(self, name, type_=str, default=None):
        self.name = name
        self.type_ = type_

        if default is not None:
            if not isinstance(default, type_):
                raise ValueError("default value is not of the required type")
        self.default = default


def login_required(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            self.raise_error(403, 0, msg='please login')
        return func(self, *args, **kwargs)

    return wrapper


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db = self.application.db
        self.session = Session(self)
        self.user_uuid = None

        self.response = {'status': 0, 'msg': ''}

    @coroutine
    def prepare(self):
        user_uuid = self.get_secure_cookie("user_uuid")
        if user_uuid:
            self.user_uuid = user_uuid.decode()
            self.current_user = self.get_current_user()
        else:
            self.set_random_user_cookie()

        yield self.session.prepare()

    def set_random_user_cookie(self):
        self.user_uuid = uuid.uuid4().hex
        self.set_secure_cookie("user_uuid", self.user_uuid)

    def get_current_user(self):
        return self.db.query(User).filter_by(uuid=self.user_uuid).first()

    @coroutine
    def login(self, user):
        if not self.current_user:
            yield self.session.rename(user.uuid)
            self.current_user = user
            self.user_uuid = user.uuid
            self.set_secure_cookie("user_uuid", self.user_uuid)

    def logout(self):
        if self.current_user:
            self.set_random_user_cookie()

    def send_email(self, receiver, subject, content):
        mailer = Email(self.application)
        mailer.write(receiver, subject, content)
        mailer.send()

    def raise_error(self, code, status=-1, msg='fail', **kwargs):
        self.set_status(code)
        self.response.update({'status': status, 'msg': msg})
        self.response.update(kwargs)
        self.write(self.response)
        self.finish()
        raise Finish()

    def start_response(self, status=1, msg='ok', **kwargs):
        self.response.update({'status': status, 'msg': msg})
        self.response.update(kwargs)
        self.write(self.response)
        self.finish()
        raise Finish()

    def parse_request_body_as_json(self):
        try:
            data = json.loads(self.request.body.decode('utf-8'))
        except Exception:
            data = {}

        return data

    @silent_return_none
    def _get_argument_outside_body(self, name, type_, default):
        if default is not None:
            value_ = self.get_argument(name, default=default)
        else:
            value_ = self.get_argument(name)

        if isinstance(value_, str) and type_ != str:
            value_ = json.loads(value_)
            if not isinstance(value_, type_):
                msg = '%s<%r> cannot be converted to type %s' % (name, value_, type_)
                raise TypeError(msg)
        return value_

    @silent_return_none
    def _get_argument_within_body(self, name, type_, default):
        data = self.parse_request_body_as_json()
        if default is not None:
            value_ = data.get(name, default)
        else:
            value_ = data.get(name)
        if isinstance(value_, str) and type_ != str:
            value_ = json.loads(value_)
            if not isinstance(value_, type_):
                msg = '%s<%r> cannot be converted to type %s' % (name, value_, type_)
                raise TypeError(msg)
        return value_

    def parse_arguments(self, required_arguments):
        argument_values = []
        for argument in required_arguments:
            try:
                value = self._get_argument_outside_body(argument.name, argument.type_, argument.default)
                if value is None:
                    value = self._get_argument_within_body(argument.name, argument.type_, argument.default)
                if value is None:
                    self.raise_error(400, -1, msg='%s is required' % argument.name)
            except TypeError as e:
                msg = str(e)
                self.raise_error(400, -1, msg=msg)
            else:
                argument_values.append(value)
        return argument_values

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.

        Requires the `.stream_request_body` decorator.
        """
        pass


class WSBaseHandler(BaseHandler, WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message('WebSocket Connected!')

    def data_received(self, chunk):
        """Implement this method to handle streamed request data.

        Requires the `.stream_request_body` decorator.
        """
        pass

    def on_message(self, message):
        """Handle incoming messages on the WebSocket

        This method must be overridden.
        """
        raise NotImplementedError
