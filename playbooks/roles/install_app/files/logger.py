"""
References:
    https://stackoverflow.com/questions/34588421/how-to-log-to-journald-systemd-via-python
    https://blog.muya.co.ke/configuring-multiple-loggers-python/
"""
import logging
import sys
import os

from dotenv import load_dotenv
load_dotenv()

logger_stdout = logging.getLogger('stdout')
logger_stderr = logging.getLogger('stderr')
logger_retweet_file = logging.getLogger('retweet')
logger_retweet_error_file = logging.getLogger('error')

logger_stdout.setLevel(logging.INFO)
logger_stderr.setLevel(logging.WARNING)
logger_retweet_file.setLevel(logging.INFO)
logger_retweet_error_file.setLevel(logging.WARNING)

# formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s]: %(message)s in %(pathname)s:%(lineno)d")
formatter = logging.Formatter(fmt="%(asctime)s [%(levelname)s]: %(message)s :%(lineno)d")

handler_stdout = logging.StreamHandler(stream=sys.stdout)
handler_stderr = logging.StreamHandler(stream=sys.stderr)
handler_retweet_file = logging.FileHandler(os.getenv('RETWEET_LOG'))
handler_retweet_error_file = logging.FileHandler(os.getenv('RETWEET_ERROR_LOG'))

handler_stdout.setFormatter(formatter)
handler_stderr.setFormatter(formatter)
handler_retweet_file.setFormatter(formatter)
handler_retweet_error_file.setFormatter(formatter)

logger_stdout.addHandler(handler_stdout)
logger_stderr.addHandler(handler_stderr)
logger_retweet_file.addHandler(handler_retweet_file)
logger_retweet_error_file.addHandler(handler_retweet_error_file)

# vim: ai et ts=4 sw=4 sts=4 nu
