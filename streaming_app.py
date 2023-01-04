import json
import logging
import os
import sys
import tweepy

from dotenv import load_dotenv

load_dotenv()
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'no').lower() == 'yes'
LOGGING_FILE_NAME = os.getenv('LOGGING_FILE_NAME', '/tmp/debug.log')
LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
PATH_TO_RECORD_RETWEETS_ID = os.environ.get('PATH_TO_RECORD_RETWEETS_ID', '/tmp/retweeted_ids')

BEARER_TOKEN = os.getenv('BEARER_TOKEN')
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

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

def create_client():  # API v2
    client = tweepy.Client(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET)

    logging.info("client created")

    return client

def get_stream_rules():
    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in IDS_TO_FOLLOW_LIST]

    return stream_rules

IDS_TO_FOLLOW = os.getenv('IDS_TO_FOLLOW', '')
IDS_TO_FOLLOW_LIST = create_list(IDS_TO_FOLLOW)
logging.debug(f'IDS_TO_FOLLOW: {IDS_TO_FOLLOW}')
if not IDS_TO_FOLLOW_LIST:
    logging.error("""

    Yikes! There are no IDs to follow!!
    Exiting!!!

    """)
    sys.exit()

IDS_NOT_TO_RETWEET_ANYTHING = os.getenv('IDS_NOT_TO_RETWEET_ANYTHING', '')
IDS_NOT_TO_RETWEET_ANYTHING_LIST = create_list(IDS_NOT_TO_RETWEET_ANYTHING)
logging.debug(f'IDS_NOT_TO_RETWEET_ANYTHING: {IDS_NOT_TO_RETWEET_ANYTHING_LIST}')

IDS_TO_RETWEET_RETWEETS = os.getenv('IDS_TO_RETWEET_RETWEETS', '')
IDS_TO_RETWEET_RETWEETS_LIST = create_list(IDS_TO_RETWEET_RETWEETS)
logging.debug(f'IDS_TO_RETWEET_RETWEETS: {IDS_TO_RETWEET_RETWEETS_LIST}')

IDS_TO_RETWEET_QUOTES = os.getenv('IDS_TO_RETWEET_QUOTES', '')
IDS_TO_RETWEET_QUOTES_LIST = create_list(IDS_TO_RETWEET_QUOTES)
logging.debug(f'IDS_TO_RETWEET_QUOTES: {IDS_TO_RETWEET_QUOTES_LIST}')

IDS_TO_REWTWEET_REPLIES = os.getenv('IDS_TO_REWTWEET_REPLIES', '')
IDS_TO_REWTWEET_REPLIES_LIST = create_list(IDS_TO_REWTWEET_REPLIES)
logging.debug(f'IDS_TO_REWTWEET_REPLIES: {IDS_TO_REWTWEET_REPLIES_LIST}')


# Touch a file
with open(PATH_TO_RECORD_RETWEETS_ID, 'a') as fh: 
    pass

def check_if_already_retweeted(tweet_id):
    with open(PATH_TO_RECORD_RETWEETS_ID, 'r') as fh:
        data = fh.read().splitlines()

    if str(tweet_id) in data:
        return True
    else:
        return False

def add_retweet_to_file(tweet_id):
    with open(PATH_TO_RECORD_RETWEETS_ID, 'a') as fh:
        fh.write(f'{tweet_id}\n')

class CustomStreamingClient(tweepy.StreamingClient):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_to_retweet = create_client()
        logging.debug(f'client_to_retweet: {self.client_to_retweet}')

    def on_tweet(self, tweet):
        logging.info(f'{"#"*20} Start {"#"*20}') 
        logging.info(f'tweet.author_id: {tweet.author_id}')
        logging.info(f'tweet.id: {tweet.id}')
        logging.info(f'tweet: {tweet}')
        logging.debug(f'tweet.referenced_tweets: {tweet.referenced_tweets}')
        logging.debug(f'tweet.data: {tweet.data}')
        #logging.debug(f'tweet.in_reply_to_user_id: {tweet.in_reply_to_user_id}')
        #logging.debug(f'{dir(tweet)}')

        verified = False
        retweet = False
        tweet_type = None
        referenced_tweet_id = None

        while not verified:
            if tweet.in_reply_to_user_id:
                logging.info('This tweet is a Reply')
                verified = True
                tweet_type = 'reply'
                if tweet.author_id in IDS_TO_REWTWEET_REPLIES_LIST:
                    logging.info('The author_id of this Reply is in the list to retweet replies')
                    retweet = True

                    # Not tested yet
                    #add_retweet_to_file(tweet.id)
                else:
                    logging.info('The author_id of this Reply is NOT in the list to retweet replies')

                break

            # For Retweet or Comment (Quote)
            if tweet.referenced_tweets:
                verified = True
                for ea in tweet.referenced_tweets:
                    if ea.type == 'quoted':
                        logging.info('This is a Quote')
                        tweet_type = 'quote'
                        if tweet.author_id in IDS_TO_RETWEET_QUOTES_LIST:
                            logging.info('The author_id of this Quote is in the list to retweet quotes')

                            if check_if_already_retweeted(ea.id):
                                logging.info('The original tweet of this Retweet has already been retweeted')
                                retweet = False
                            else:
                                retweet = True
                                add_retweet_to_file(ea.id)
                        else:
                            logging.info('The author_id of this Quote is NOT in the list to retweet quotes')

                    if ea.type == 'retweeted':
                        logging.info('This is a Retweet')
                        tweet_type = 'retweet'
                        if tweet.author_id in IDS_TO_RETWEET_RETWEETS_LIST:
                            logging.info('The author_id of this Retweet is in the list to retweet retweets')

                            if check_if_already_retweeted(ea.id):
                                logging.info('The original tweet of this Retweet has already been retweeted')
                                retweet = False
                            else:
                                retweet = True
                                add_retweet_to_file(ea.id)
                        else:
                            logging.info('The author_id of this Retweet is NOT in the list to retweet retweets')
                break

            else:
                verified = True
                retweet = True
                logging.info('This is a simple Tweet')
                tweet_type = 'simple'
                add_retweet_to_file(tweet.id)

        #logging.debug(f'{tweet.author_id} -- {IDS_NOT_TO_RETWEET_ANYTHING_LIST}')
        #logging.debug(f'{type(tweet.author_id)} -- {type(IDS_NOT_TO_RETWEET_ANYTHING_LIST)}')
        if tweet.author_id in IDS_NOT_TO_RETWEET_ANYTHING_LIST:
            logging.info('The author_id of this Tweet is in the list to NOT retweet ANYTHING')
            retweet = False

        logging.debug(f'Verified: {verified}')
        logging.info(f'Retweet: {retweet}')

        if retweet and verified:
            # One last check
            if tweet.author_id in IDS_TO_FOLLOW_LIST:
                retweet_response = self.client_to_retweet.retweet(tweet_id=tweet.id)
                logging.debug(f'retweet_response: {retweet_response}')
                logging.info(f'retweet_response.data: {retweet_response.data}')
                logging.info(f'retweet_response.errors: {retweet_response.errors}')
            else:
                logging.error(f'Yikes!! How did this tweet even get here!!')


        if not verified:
            logging.warning('Not Verified:  How did this get here labeled "unverified"')

        if not retweet:
            logging.info(f'Not retweeted: retweet={retweet}, tweet_id={tweet.id}')


        logging.debug(f'{"#"*20} END {"#"*20}') 

    def on_includes(self, includes):
        logging.info(f'includes: {includes}')

    def on_data(self, raw_data):
        super().on_data(raw_data)

        return
        my_data = json.loads(raw_data)
        logging.debug(f'json.loads: {my_data}')
            

def main():
    try:
        msg = '########## Starting tweepy.StreamClient ##########'
        logging.info(msg)

        stream_rules = get_stream_rules()
        logging.info(f'Stream rules: {stream_rules}')

        streaming_client = CustomStreamingClient(BEARER_TOKEN)
        streaming_client.add_rules(add=stream_rules)  # only need to do once it appears, but no harm in calling it

        current_stream_rules = streaming_client.get_rules()
        logging.info(f'Current stream rules: {stream_rules}')

        streaming_client.filter(expansions=['author_id'], user_fields=['username', 'name'],
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
