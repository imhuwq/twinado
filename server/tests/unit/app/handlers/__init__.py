from server.application import API

test = API(name='test', prefix='/test/v1')

from .session import session
from .user import user
from .xsrf import xsrf
from .email import email
