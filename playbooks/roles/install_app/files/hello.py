import logging
import os
from time import sleep

from dotenv import load_dotenv


load_dotenv()
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'no').lower() == 'yes'
LOGGING_FILE_NAME = os.getenv('LOGGING_FILE_NAME', '/tmp/debug.log')
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()


if LOG_TO_FILE:
    logging.basicConfig(level=LOGLEVEL,
            format='%(asctime)s [%(levelname)s]: %(message)s', filename=LOGGING_FILE_NAME)
else:
    logging.basicConfig(level=LOGLEVEL,
            format='%(asctime)s [%(levelname)s]: %(message)s')

while True:
    logging.info("Hello World")
    sleep(60 * 10)

# vim: ai et ts=4 sw=4 sts=4 nu

