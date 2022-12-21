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
    return list(filter(None, [int(ea) for ea in string_list.split(',')]))

def get_stream_rules():
    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in IDS_TO_FOLLOW_LIST]

    return stream_rules

bearer_token = os.getenv('BEARER_TOKEN')

IDS_TO_FOLLOW = os.getenv('IDS_TO_FOLLOW')
IDS_TO_FOLLOW_LIST = create_list(IDS_TO_FOLLOW)
logging.debug(IDS_TO_FOLLOW_LIST)
logging.debug(type(IDS_TO_FOLLOW_LIST))

IDS_NOT_PUBLISH = os.getenv('IDS_NOT_TO_PUBLISH')
IDS_NOT_TO_PUBLISH = create_list(IDS_TO_FOLLOW)
logging.debug(IDS_NOT_TO_PUBLISH)
logging.debug(type(IDS_NOT_TO_PUBLISH))


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
        publish = False

        while not verified:
            if tweet.in_reply_to_user_id:
                logging.debug('This tweet is a reply')
            else:
                logging.debug('This tweet is NOT a reply')

            # For Retweet or Comment (Quote)
            if 'referenced_tweets' in tweet.data.keys():
                for ea in tweet.data['referenced_tweets']:
                    if ea['type'] == 'quoted':
                        logging.debug('This is a quote')
                    if ea['type'] == 'retweeted':
                        logging.debug('This is a retweet')

                    if int(tweet.author_id) not in IDS_NOT_TO_PUBLISH:
                        if ea.id in IDS_TO_FOLLOW_LIST:
                            logging.debug('This retreat or quote should already have been "seen"')
                            verified = True
                            publish = False
                            break
            else:
                verified = True
                publish = True
                logging.debug('This is a simple tweet, i.e. not a Reply, Retweet, nor Comment ("Quoted Tweet")')

            if int(tweet.author_id) in IDS_NOT_TO_PUBLISH:
                logging.debug('The author_id of this tweet is in the list not to publish')
                verified = True
                publish = False
                break

        logging.debug(f'Verified: {verified}')
        logging.debug(f'Publish: {publish}')
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
