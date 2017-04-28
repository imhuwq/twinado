# encoding: utf-8

"""
twinado server.extensions.email

~~~~~~

基于 python 标准库的邮件插件, 在异步线程中发送邮件

"""

import smtplib
from email.mime.text import MIMEText

from threading import Thread


class Email:
    def __init__(self, app=None):
        self.app = app

        self.sender = None
        self.user = None
        self.password = None
        self.host = None
        self.port = None

        self.receiver = None
        self.subject = None
        self.content = None

        self.msg = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app

        email_settings = app.settings.get("email_config")

        self.sender = email_settings.get("user")
        self.user = email_settings.get("user")
        self.password = email_settings.get("password")
        self.host = email_settings.get("host")
        self.port = email_settings.get("port")

        self.receiver = None
        self.subject = None
        self.content = None

        self.msg = None

    def write(self, receiver, subject, content):
        self.receiver = receiver
        self.subject = subject
        self.content = content

        self.msg = MIMEText(content)
        self.msg["Subject"] = self.subject
        self.msg["From"] = self.sender
        self.msg["To"] = self.receiver

    def _send(self):
        if isinstance(self.msg, MIMEText):
            server = smtplib.SMTP_SSL(self.host, self.port)
            server.login(self.sender, self.password)
            server.sendmail(self.sender, self.receiver, msg=self.msg.as_string())
            server.quit()
        else:
            raise Exception("Please write your message before you send it")

    def send(self):
        thread = Thread(target=self._send)
        thread.start()
