"""
References:
    https://stackoverflow.com/questions/34588421/how-to-log-to-journald-systemd-via-python
    https://blog.muya.co.ke/configuring-multiple-loggers-python/
"""
import logging
import sys
from time import sleep

import tweepy

logger_stdout = logging.getLogger('hello_world.stdout')
logger_stderr = logging.getLogger('hello_world.stderr')

logger_stdout.setLevel(logging.INFO)
logger_stderr.setLevel(logging.WARNING)

formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")

handler_stdout = logging.StreamHandler(stream=sys.stdout)
handler_stderr = logging.StreamHandler(stream=sys.stderr)

handler_stdout.setFormatter(formatter)
handler_stderr.setFormatter(formatter)

logger_stdout.addHandler(handler_stdout)
logger_stderr.addHandler(handler_stderr)

while True:
    logger_stdout.info('hello world')
    logger_stderr.warning('blue moon')

    sleep(60 * 2)

