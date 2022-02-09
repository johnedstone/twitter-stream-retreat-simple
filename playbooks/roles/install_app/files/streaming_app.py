"""
References:
    https://docs.tweepy.org/en/stable/examples.html
    https://docs.tweepy.org/en/stable/api.html
    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    https://realpython.com/twitter-bot-python-tweepy/#creating-twitter-api-authentication-credentials
    https://python.plainenglish.io/how-to-create-a-twitter-retweet-bot-using-python-e2cac0f2cab7
"""
import tweepy
import os
import sys

from config import create_api
from dotenv import load_dotenv
from get_user_screen_name import get_screen_name

load_dotenv()

from logger import (
    logger_stdout,
    logger_stderr,
    logger_retweet_file,
    logger_retweet_error_file
)

api = create_api()
credentials = api.verify_credentials()

consumer_key = os.getenv('API_KEY')
consumer_secret = os.getenv('API_KEY_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

ids_to_follow_list = []
ids_to_follow = os.getenv('IDS_TO_FOLLOW')
if ids_to_follow:
    ids_to_follow_list = [int(ea) for ea in ids_to_follow.split(',')] #, 38531358]

ids_to_publish_only_tweets_list = []
ids_to_publish_only_tweets = os.getenv('IDS_TO_PUBLISH_ONLY_TWEETS')
if ids_to_publish_only_tweets:
    ids_to_publish_only_tweets_list = [int(ea) for ea in ids_to_publish_only_tweets.split(',')]

ids_to_publish_tweets_and_quotes_list = []
ids_to_publish_tweets_and_quotes = os.getenv('IDS_TO_PUBLISH_TWEETS_AND_QUOTES')
if ids_to_publish_tweets_and_quotes:
    ids_to_publish_tweets_and_quotes_list = [int(ea) for ea in ids_to_publish_tweets_and_quotes.split(',')]

def check_ids_to_follow():
    if not ids_to_follow_list:
        logger_stderr.error('Fatal: No user accounts to follow!  Yikes!!!')
        logger_retweet_error_file.error('Fatal: No user accounts to follow!  Yikes')
        raise SystemExit
    else:
        msg = f'''{"Following:":40}{[get_screen_name(ea) for ea in ids_to_follow_list]}'''
        logger_retweet_file.info(msg)
        logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)

        msg = f'''{"Retweeting only tweets:":40}{[get_screen_name(ea) for ea in ids_to_publish_only_tweets_list]}'''
        logger_retweet_file.info(msg)
        logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)

        msg = f'''{"Retweeting tweets and quotes:":40}{[get_screen_name(ea) for ea in ids_to_publish_tweets_and_quotes_list]}'''
        logger_retweet_file.info(msg)
        logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)

        not_restricted_ids = ids_to_follow_list
        for ea in ids_to_publish_only_tweets_list:
            not_restricted_ids.remove(ea)

        for ea in ids_to_publish_tweets_and_quotes_list:
            not_restricted_ids.remove(ea)

        msg = f'''{"Retweeting tweets, quotes and retweets:":40}{[get_screen_name(ea) for ea in not_restricted_ids]}'''
        logger_retweet_file.info(msg)
        logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)
    

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        """
        https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
        """
        try:
            publish = False
            log_msg = True
            tweet_type = None
            is_retweet = hasattr(status, 'retweeted_status')
            is_quote = status.is_quote_status

            logger_retweet_file.info(f'tweet id: {status.id}')

            if status.user.id == credentials.id:
                tweet_type = 'Apps own retweet'

            if status.in_reply_to_status_id:
                tweet_type = 'Reply'

            if not is_retweet and not is_quote:
                publish = True
                tweet_type = 'Simple Tweet'

            if not is_retweet and is_quote:
                tweet_type = 'Simple Quote'
                if status.user.id not in ids_to_publish_only_tweet_list:
                    publish = True

            if is_retweet:
                tweet_type = 'Retweet'
                if is_quote:
                    tweet_type = tweet_type + ' with Quote'

                if status.user.id not in ids_to_publish_only_tweets_list:
                    if status.user.id not in ids_to_publish_tweets_and_quotes_list:
                        publish = True

            if publish:
                r = api.retweet(status.id)

        except Exception as e:
            logger_stderr.warning('IDPrinter error - {} - {}'.format(type(e).__name__, e))
            logger_retweet_error_file.warning('IDPrinter error - {} - {}'.format(type(e).__name__, e))

        finally:
            if log_msg:
                msg = f'' \
                      f'Published: {publish} - ' \
                      f'Tweet Type: {tweet_type:20} - ' \
                      f'''{status.user.screen.name:12} - ''' \
                      f'''{status.id:12} - ''' \
                      f'''{status.text}''' \
                      f''
                logger_retweet_file.info(msg)

def main():
    try:
        # Initialize instance of the subclass
        logger_stderr.warning('Starting tweepy.Stream')
        logger_retweet_error_file.warning('Starting tweepy.Stream')

        check_ids_to_follow()

        printer = IDPrinter(
          consumer_key, consumer_secret,
          access_token, access_token_secret,
        )
        
        printer.filter(follow=ids_to_follow_list)
    
    except Exception as e:
        logger_stderr.error('Stream error - {} - {}'.format(type(e).__name__, e))
        logger_retweet_error_file.error('Stream error - {} - {}'.format(type(e).__name__, e))

if __name__ == '__main__':
    try:    
        main()
    except KeyboardInterrupt:
        logger_stderr.warning("""
        Closing ...
        """)

# vim: ai et ts=4 sw=4 sts=4 nu
