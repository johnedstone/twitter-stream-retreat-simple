import json
import logging
import os
import sys
import tweepy

from dotenv import load_dotenv

load_dotenv()
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'no').lower() == 'yes'
LOGGING_FILE_NAME = os.getenv('LOGGING_FILE_NAME', 'debug.log')
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()


if LOG_TO_FILE:
    logging.basicConfig(level=LOGLEVEL,
            format='%(asctime)s [%(levelname)s]: %(message)s', filename=LOGGING_FILE_NAME)
else:
    logging.basicConfig(level=LOGLEVEL,
            format='%(asctime)s [%(levelname)s]: %(message)s')

def create_list(string_list):
    list_to_return = list(filter(None, string_list.split(',')))
    if list_to_return:
        list_to_return = [int(ea) for ea in list_to_return]

    return list_to_return

def get_stream_rules():
    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in IDS_TO_FOLLOW_LIST]

    return stream_rules

bearer_token = os.getenv('BEARER_TOKEN')

IDS_TO_FOLLOW = os.getenv('IDS_TO_FOLLOW', '')
IDS_TO_FOLLOW_LIST = create_list(IDS_TO_FOLLOW)
logging.debug(f'IDS_TO_FOLLOW (to Retweet Simple Tweets): {IDS_TO_FOLLOW_LIST}')
if not IDS_TO_FOLLOW_LIST:
    logging.error("""

    Yikes! There are no IDs to follow!!
    Exiting!!!

    """)
    sys.exit()

IDS_NOT_TO_RETWEET = os.getenv('IDS_NOT_TO_RETWEET', '')
IDS_NOT_TO_RETWEET_LIST = create_list(IDS_NOT_TO_RETWEET)
logging.debug(f'IDS_NOT_TO_RETWEET: {IDS_NOT_TO_RETWEET_LIST}')

IDS_NOT_TO_RETWEET_RETWEETS = os.getenv('IDS_NOT_TO_RETWEET_RETWEETS', '')
IDS_NOT_TO_RETWEET_RETWEETS_LIST = create_list(IDS_NOT_TO_RETWEET_RETWEETS)
logging.debug(f'IDS_NOT_TO_RETWEET_RETWEETS: {IDS_NOT_TO_RETWEET_RETWEETS_LIST}')

IDS_NOT_TO_RETWEET_QUOTES = os.getenv('IDS_NOT_TO_RETWEET_QUOTES', '')
IDS_NOT_TO_RETWEET_QUOTES_LIST = create_list(IDS_NOT_TO_RETWEET_QUOTES)
logging.debug(f'IDS_NOT_TO_RETWEET_QUOTES: {IDS_NOT_TO_RETWEET_QUOTES_LIST}')

IDS_NOT_TO_RETWEET_REPLIES = os.getenv('IDS_NOT_TO_RETWEET_REPLIES', '')
IDS_NOT_TO_RETWEET_REPLIES_LIST = create_list(IDS_NOT_TO_RETWEET_REPLIES)
logging.debug(f'IDS_NOT_TO_RETWEET_REPLIES: {IDS_NOT_TO_RETWEET_REPLIES_LIST}')


class CustomStreamingClient(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        logging.debug(f'{"#"*20} Start {"#"*20}') 
        logging.debug(f'tweet: {tweet}')
        logging.debug(f'tweet.data: {tweet.data}')
        logging.debug(f'tweet.author_id: {tweet.author_id}')
        logging.debug(f'tweet.in_reply_to_user_id: {tweet.in_reply_to_user_id}')
        logging.debug(f'tweet.referenced_tweets: {tweet.referenced_tweets}')
        logging.debug(f'{dir(tweet)}')

        verified = False
        retweet = False

        while not verified:
            if tweet.in_reply_to_user_id:
                logging.debug('This tweet is a reply')
                if tweet.author_id in IDS_NOT_TO_RETWEET_REPLIES_LIST:
                    logging.debug('The author_id of this reply is in the list not to retweet replies')
                    verified = True
                    retweet = False
                    break
            else:
                logging.debug('This tweet is NOT a reply')

            # For Retweet or Comment (Quote)
            if 'referenced_tweets' in tweet.data.keys():
                for ea in tweet.data['referenced_tweets']:
                    if ea['type'] == 'quoted':
                        logging.debug('This is a quote')
                        if tweet.author_id in IDS_NOT_TO_RETWEET_QUOTES_LIST:
                            logging.debug('The author_id of this Quote is in the list not to retweet quotes')
                            verified = True
                            retweet = False
                            break
                    if ea['type'] == 'retweeted':
                        logging.debug('This is a retweet')
                        if tweet.author_id in IDS_NOT_TO_RETWEET_RETWEETS_LIST:
                            logging.debug('The author_id of this Retweet is in the list not to retweet retweets')
                            verified = True
                            retweet = False
                            break

                    if int(ea['id']) in IDS_TO_FOLLOW_LIST:
                        logging.debug('This retreat or quote should already have been "seen"')
                        verified = True
                        retweet = False
                        break
                # ... then "retweet":w
                verified = True
                retweet = False
            else:
                verified = True
                retweet = True
                logging.debug('This is a simple tweet, i.e. not a Reply, Retweet, nor Comment ("Quoted Tweet")')

        logging.debug(f'{type(tweet.author_id)} -- {type(IDS_NOT_TO_RETWEET_LIST)}')
        if tweet.author_id in IDS_NOT_TO_RETWEET_LIST:
            logging.debug('The author_id of this tweet is in the list not to retweet')
            verified = True
            retweet = False

        logging.debug(f'Verified: {verified}')
        logging.debug(f'Retweet: {retweet}')
        logging.debug(f'{"#"*20} END {"#"*20}') 

    def on_includes(self, includes):
        logging.debug(f'includes {includes}')

    def on_data(self, raw_data):
        super().on_data(raw_data)

        my_data = json.loads(raw_data)
        logging.debug(f'json.loads: {my_data}')
            

def main():
    try:
        msg = '########## Starting tweepy.StreamClient ##########'
        logging.info(msg)

        stream_rules = get_stream_rules()
        logging.info(f'Stream rules: {stream_rules}')

        streaming_client = CustomStreamingClient(bearer_token)
        streaming_client.add_rules(add=stream_rules)  # only need to do once it appears, but no harm in calling it

        current_stream_rules = streaming_client.get_rules()
        logging.info(f'Current stream rules: {stream_rules}')

        streaming_client.filter(expansions=['author_id'], user_fields=['username'],
                tweet_fields=['in_reply_to_user_id', 'referenced_tweets'])
        #streaming_client.filter()
    
    except KeyboardInterrupt:
        streaming_client.session.close()
        streaming_client.running = False
        streaming_client.on_disconnect()
        logging.warning('Keyboard Interrupt... closing')
    except Exception as e:
        msg = f'Streaming client error: {e}'
        logging.error(msg)

if __name__ == '__main__':
    try:    
        main()
    except KeyboardInterrupt:
        logging.warning("""
        Closing ...
        """)

# vim: ai et ts=4 sw=4 sts=4 nu
