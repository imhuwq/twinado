# encoding: utf-8

"""
twinado manager.py

~~~~~~

twinado console commands

type `python manager.py --help` to see what you get
"""

import logging
import signal
import time

import click
from tornado import httpserver, ioloop
from tornado import log as tornado_log

from server.instance.tornado_config import PERMITTED_MODES

from server.application import create_app
from server.resources.api_v1 import apiv1
from server.tests import UnitTest


@click.group()
def manager():
    pass


@manager.command(help="执行单元测试")
@click.option("--name", "name", default=".", type=click.STRING,
              help="指定需要执行的单元测试: "
                   "--name=model.user.UserModelTest.test_user_auth_token")
def unittest(name):
    unit_test = UnitTest(name)
    unit_test.run()


@manager.command(help="开启 Tornado web 服务器")
@click.option("--port", "port", default=8000, type=click.INT,
              help="指定服务器运行的端口, 默认 8000")
@click.option("--mode", "mode", default="production", type=click.Choice(PERMITTED_MODES),
              help="指定服务器运行模式, 默认 production")
def runserver(port, mode):
    def sig_handler(sig, frame):
        logging.info('Caught signal: %s', sig)
        ioloop.IOLoop.instance().add_callback(shutdown)

    def shutdown():
        logging.warning('shutting down server...')
        http_server.stop()

        logging.warning('shutting down server in 3 seconds ...')
        io_loop = ioloop.IOLoop.instance()

        deadline = time.time() + 3

        def stop_loop():
            now = time.time()
            if now < deadline and (io_loop._callbacks or io_loop._timeouts):
                io_loop.add_timeout(now + 1, stop_loop)
            else:
                logging.warning('shutting down IO Loop...')
                io_loop.stop()

        stop_loop()

    tornado_log.enable_pretty_logging()
    app = create_app(apiv1.handlers, mode=mode)
    app.settings['login_url'] = app.reverse_url('api_v1.user.UserLogin')

    global http_server
    http_server = httpserver.HTTPServer(app)
    http_server.listen(port)

    signal.signal(signal.SIGQUIT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)

    logging.info('[%s]: listening on 127.0.0.1:%s' % (mode, port))
    ioloop.IOLoop.instance().start()

    logging.warning("Tornado server has been shut down completely")


if __name__ == "__main__":
    manager()
