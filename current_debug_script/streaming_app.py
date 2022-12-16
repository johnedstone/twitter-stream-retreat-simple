import logging
import os
import sys
import tweepy

from dotenv import load_dotenv

load_dotenv()

"""
>>> client.filter()
"""

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s', filename='debug.log')

bearer_token = os.getenv('BEARER_TOKEN')
client = tweepy.StreamingClient(bearer_token)

ids_to_follow_list = []
ids_to_follow = os.getenv('IDS_TO_FOLLOW')
if ids_to_follow:
    ids_to_follow_list = [int(ea) for ea in ids_to_follow.split(',')]

def get_stream_rules():
    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in ids_to_follow_list]

    return stream_rules

stream_rules = get_stream_rules()
#logging.info(f'Stream rules: {stream_rules}')

#client.add_rules(add=stream_rules)  # only need to do once it appears
current_stream_rules = client.get_rules()
logging.info(f'Current stream rules: {stream_rules}')
client.filter()

#-## vim: ai et ts=4 sw=4 sts=4 nu
