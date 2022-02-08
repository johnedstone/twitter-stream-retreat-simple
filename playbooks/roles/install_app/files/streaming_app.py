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
load_dotenv()

from logger import (
    # logger_stdout, # not using
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

twitter_ids_list = []
twitter_ids = os.getenv('TWEET_STATUS_USER_IDS_TO_RETWEET')
if twitter_ids:
    twitter_ids_list = [int(ea) for ea in twitter_ids.split(',')] #, 38531358]
tweet_status_user_ids_to_retweet = twitter_ids_list

exemptions_list = []
exemptions = os.getenv('RETWEET_EXEMPTIONS')
if exemptions:
    exemptions_list = [int(ea) for ea in exemptions.split(',')]
retweet_exemptions = exemptions_list

def check_twitter_ids():
    if not tweet_status_user_ids_to_retweet:
        logger_stderr.error('Fatal: No twitter accounts to follow!  Yikes!!!')
        logger_retweet_error_file.error('Fatal: No twitter accounts to follow!  Yikes')
        raise SystemExit
    else:
        logger_retweet_file.info('Current status.user.ids following: {}'.format(tweet_status_user_ids_to_retweet))
        logger_retweet_error_file.warning('Current status.user.ids following: {}'.format(tweet_status_user_ids_to_retweet))
    
    if not retweet_exemptions:
        logger_stderr.warning('Warning: No retweet exemptions.  Are you okay with this?')
        logger_retweet_error_file.warning('Warning: No retweet exemptions.  Are you okay with this?')
    else:
        logger_retweet_file.info('Current retweet_exemptions: {}'.format(retweet_exemptions))
        logger_retweet_error_file.warning('Current retweet_exemptions: {}'.format(retweet_exemptions))

# Subclass Stream to print IDs of Tweets received
class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        """
        https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
        """
        try:
            retweet = False
            tweet_type = None
            apps_own_retweet = False
            is_retweet = hasattr(status, 'retweeted_status')

            if status.user.id == credentials.id:
                apps_own_retweet = True
            elif status.in_reply_to_status_id:
                tweet_type = 'Reply'
            elif status.is_quote_status and is_retweet and \
                    status.retweeted_status.user.id in tweet_status_user_ids_to_retweet:
                tweet_type = 'Already retweeted'  # this "is_retweet" may be redundant as perhaps a quote is always a retweet
            elif status.is_quote_status:
                tweet_type = 'Quote'
                retweet = True
            elif is_retweet:
                if status.user.id in retweet_exemptions:
                    retweet = True
                    tweet_type = 'Exempted retweet'
                else:
                    tweet_type = 'Retweet'
            else:
                tweet_type = 'Tweet'
                retweet = True

            if retweet:
                r = api.retweet(status.id)

        except Exception as e:
            logger_stderr.warning('IDPrinter error - {} - {}'.format(type(e).__name__, e))
            logger_retweet_error_file.warning('IDPrinter error - {} - {}'.format(type(e).__name__, e))

        finally:
            if not apps_own_retweet:
                logger_retweet_file.info('{} - {} - Retweeted: {} - {}'.format(status.user.screen_name, tweet_type, retweet, status.text))

def main():
    try:
        # Initialize instance of the subclass
        logger_stderr.warning('Starting tweepy.Stream')
        logger_retweet_error_file.warning('Starting tweepy.Stream')

        check_twitter_ids()

        printer = IDPrinter(
          consumer_key, consumer_secret,
          access_token, access_token_secret,
        )
        
        printer.filter(follow=tweet_status_user_ids_to_retweet)
    
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
