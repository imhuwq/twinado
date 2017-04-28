# encoding: utf-8

"""
twinado deploy.utils.console

~~~~~~

twinado 部署时 console 相关的工具

"""


class ConsoleColor:
    NC = '\033[0m'  # white (normal)
    RED = '\033[31m'  # red
    GREEN = '\033[32m'  # green
    ORANGE = '\033[33m'  # orange
    BLUE = '\033[34m'  # blue
    PURPLE = '\033[35m'  # purple


def colorize(word, color):
    result = "%s%s%s" % (color, word, ConsoleColor.NC)
    return result


init = colorize("init", ConsoleColor.BLUE)
good = colorize("good", ConsoleColor.GREEN)
fail = colorize("fail", ConsoleColor.RED)


def notify(status, description):
    print("\n[%s] %s\n" % (status.ljust(13, " "), description))
