import logging
import tweepy
import os
import sys

from config import create_client
from dotenv import load_dotenv
#from get_user_screen_name import get_screen_name

load_dotenv()

LOG_FILENAME = os.getenv('LOG_FILENAME')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'WARNING').upper()

FORMAT = '%(asctime)s %(module)s [%(levelname)s]: %(message)s'
if LOG_FILENAME:
    logging.basicConfig(level=LOG_LEVEL, format=FORMAT, filename=LOG_FILENAME)
else:
    logging.basicConfig(level=LOG_LEVEL, format=FORMAT)
log = logging.getLogger(__name__)

client = create_client() # will use later for retweeting

sys.exit('Exiting .... work in progress')

#-#bearer_token = os.getenv('BEARER_TOKEN')
#-#
#-#include_replys_and_self_retweets_in_log = os.getenv('INCLUDE_REPLYS_AND_SELF_RETWEETS_IN_LOG')
#-#Publish_Live = os.getenv('Publish_Live', 'no') == 'yes'
#-#
#-#ids_to_follow_list = []
#-#ids_to_follow = os.getenv('IDS_TO_FOLLOW')
#-#if ids_to_follow:
#-#    ids_to_follow_list = [int(ea) for ea in ids_to_follow.split(',')]
#-#
#-#ids_to_publish_only_tweets_list = []
#-#ids_to_publish_only_tweets = os.getenv('IDS_TO_PUBLISH_ONLY_TWEETS')
#-#if ids_to_publish_only_tweets:
#-#    ids_to_publish_only_tweets_list = [int(ea) for ea in ids_to_publish_only_tweets.split(',')]
#-#
#-#ids_to_publish_tweets_and_quotes_list = []
#-#ids_to_publish_tweets_and_quotes = os.getenv('IDS_TO_PUBLISH_TWEETS_AND_QUOTES')
#-#if ids_to_publish_tweets_and_quotes:
#-#    ids_to_publish_tweets_and_quotes_list = [int(ea) for ea in ids_to_publish_tweets_and_quotes.split(',')]
#-#
#-#known_users = {}  # will populate as the app runs
#-#
#-#def check_ids_to_follow():
#-#    if not ids_to_follow_list:
#-#        msg = 'Fatal: No user accounts to follow!  Yikes!!!'
#-#        logging.error(msg)
#-#        ###logger_stderr.error(msg)
#-#        ###logger_retweet_error_file.error(msg)
#-#        raise SystemExit
#-#    else:
#-#        msg = f'''{"Following:":40}{[get_screen_name(ea) for ea in ids_to_follow_list]}'''
#-#        #logging.info(msg)
#-#        ###logger_retweet_file.info(msg)
#-#        ###logger_retweet_error_file.warning(msg)
#-#        ###logger_stdout.info(msg)
#-#
#-#        msg = f'''{"Retweeting only tweets:":40}{[get_screen_name(ea) for ea in ids_to_publish_only_tweets_list]}'''
#-#        #logging.info(msg)
#-#        ###logger_retweet_file.info(msg)
#-#        ###logger_retweet_error_file.warning(msg)
#-#        ###logger_stdout.info(msg)
#-#
#-#        msg = f'''{"Retweeting tweets and quotes:":40}{[get_screen_name(ea) for ea in ids_to_publish_tweets_and_quotes_list]}'''
#-#        #logging.info(msg)
#-#        ###logger_retweet_file.info(msg)
#-#        ###logger_retweet_error_file.warning(msg)
#-#        ###logger_stdout.info(msg)
#-#
#-#        not_restricted_ids = [ea for ea in ids_to_follow_list]
#-#        for ea in ids_to_publish_only_tweets_list:
#-#            not_restricted_ids.remove(ea)
#-#
#-#        for ea in ids_to_publish_tweets_and_quotes_list:
#-#            not_restricted_ids.remove(ea)
#-#
#-#        msg = f'''{"Retweeting tweets, quotes and retweets:":40}{[get_screen_name(ea) for ea in not_restricted_ids]}'''
#-#        #logging.info(msg)
#-#        ###logger_retweet_file.info(msg)
#-#        ###logger_retweet_error_file.warning(msg)
#-#        ###logger_stdout.info(msg)
#-#    
#-#
#-#class CustomStreamingClient(tweepy.StreamingClient):
#-#    """https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
#-#
#-#    https://developer.twitter.com/en/docs/twitter-api/fields
#-#    """
#-#
#-#    def on_request_error(self, status_code):
#-#        msg = 'custom method: on_request_error has been called ....  '
#-#        logging.info(msg)
#-#        ###logger_retweet_file.info(msg)
#-#        ###logger_stdout.info(msg)
#-#        super().on_request_error(status_code)
#-#
#-#    def on_tweet(self, tweet):
#-#        try:
#-#            publish = False
#-#            log_msg = True
#-#            tweet_type = 'Unknown'
#-#
#-#            ###logger_retweet_file.info(f'Start: tweet.id {tweet.id}')
#-#            ###logger_retweet_file.info(f'{tweet.text}')
#-#            ###logger_retweet_file.info(f'{tweet.author_id}')
#-#            ###logger_retweet_file.info(f'Which user_id is this a reply: {tweet.in_reply_to_user_id}')
#-#
#-#            if not tweet.author_id in known_users:
#-#                known_users[tweet.author_id] = get_screen_name(tweet.author_id)
#-#
#-#            msg = f'End: tweet.author_id {known_users[tweet.author_id]}'
#-#            logging.info(msg)
#-#            ###logger_retweet_file.info(msg)
#-#
#-#        except Exception as e:
#-#            msg ='Custom Streaming Client error - {} - {}'.format(type(e).__name__, e)
#-#            logging.warning(msg)
#-#            ###logger_stderr.warning('Custom Streaming Client error - {} - {}'.format(type(e).__name__, e))
#-#            ###logger_retweet_error_file.warning('Custom Streaming Client error - {} - {}'.format(type(e).__name__, e))
#-#
#-#def get_stream_rules():
#-#    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in ids_to_follow_list]
#-#
#-#    return stream_rules
#-#
#-#def main():
#-#    try:
#-#        msg = 'Starting tweepy.Stream'
#-#        ###logger_retweet_file.info(msg)
#-#        ###logger_retweet_error_file.warning(msg)
#-#
#-#        check_ids_to_follow()
#-#
#-#        streaming_client = CustomStreamingClient(bearer_token, wait_on_rate_limit=True)
#-#        stream_rules = get_stream_rules()
#-#        #streaming_client.add_rules(add=stream_rules)  # only need to do once it appears
#-#
#-#        current_stream_rules = streaming_client.get_rules()
#-#
#-#        msg = f'current stream_rules: {current_stream_rules}'
#-#        ###logger_stdout.info(msg)
#-#        ###logger_retweet_file.info(msg)
#-#
#-#        streaming_client.filter(expansions=['author_id'])
#-#    
#-#    except KeyboardInterrupt:
#-#        streaming_client.session.close()
#-#        streaming_client.running = False
#-#        streaming_client.on_disconnect()
#-#        ###logger_stderr.warning("""
#-#        logging.warning("""
#-#        streaming.session.close()
#-#        Closing ...
#-#        """)
#-#    except Exception as e:
#-#        msg = 'Stream error - {} - {}'.format(type(e).__name__, e)
#-#        logging.error(msg)
#-#        ###logger_stderr.error(msg)
#-#        ###logger_retweet_error_file.error(msg)
#-#
#-#if __name__ == '__main__':
#-#    try:    
#-#        main()
#-#    except KeyboardInterrupt:
#-#        ###logger_stderr.warning("""
#-#        logging.warning("""
#-#        Closing ...
#-#        """)
#-#
#-## vim: ai et ts=4 sw=4 sts=4 nu
