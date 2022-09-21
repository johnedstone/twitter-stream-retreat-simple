"""
References:
    https://docs.tweepy.org/en/stable/examples.html
    https://docs.tweepy.org/en/stable/api.html
    https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet
    https://developer.twitter.com/en/docs/twitter-api/data-dictionary/introduction  # API v2
    https://realpython.com/twitter-bot-python-tweepy/#creating-twitter-api-authentication-credentials
    https://python.plainenglish.io/how-to-create-a-twitter-retweet-bot-using-python-e2cac0f2cab7
"""
import tweepy
import os
import sys

from config import create_client
from dotenv import load_dotenv
from get_user_screen_name import get_screen_name

load_dotenv()

from logger import (
    logger_stdout,
    logger_stderr,
    logger_retweet_file,
    logger_retweet_error_file
)

#client = create_client()

#consumer_key = os.getenv('API_KEY')
#consumer_secret = os.getenv('API_KEY_SECRET')
#access_token = os.getenv('ACCESS_TOKEN')
#access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('BEARER_TOKEN')

include_replys_and_self_retweets_in_log = os.getenv('INCLUDE_REPLYS_AND_SELF_RETWEETS_IN_LOG')
Publish_Live = os.getenv('Publish_Live', 'no') == 'yes'

ids_to_follow_list = []
ids_to_follow = os.getenv('IDS_TO_FOLLOW')
if ids_to_follow:
    ids_to_follow_list = [int(ea) for ea in ids_to_follow.split(',')]

ids_to_publish_only_tweets_list = []
ids_to_publish_only_tweets = os.getenv('IDS_TO_PUBLISH_ONLY_TWEETS')
if ids_to_publish_only_tweets:
    ids_to_publish_only_tweets_list = [int(ea) for ea in ids_to_publish_only_tweets.split(',')]

ids_to_publish_tweets_and_quotes_list = []
ids_to_publish_tweets_and_quotes = os.getenv('IDS_TO_PUBLISH_TWEETS_AND_QUOTES')
if ids_to_publish_tweets_and_quotes:
    ids_to_publish_tweets_and_quotes_list = [int(ea) for ea in ids_to_publish_tweets_and_quotes.split(',')]

known_users = {}

def check_ids_to_follow():
    if not ids_to_follow_list:
        logger_stderr.error('Fatal: No user accounts to follow!  Yikes!!!')
        ##logger_retweet_error_file.error('Fatal: No user accounts to follow!  Yikes')
        raise SystemExit
    else:
        msg = f'''{"Following:":40}{[get_screen_name(ea) for ea in ids_to_follow_list]}'''
        ##logger_retweet_file.info(msg)
        ##logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)

        msg = f'''{"Retweeting only tweets:":40}{[get_screen_name(ea) for ea in ids_to_publish_only_tweets_list]}'''
        ##logger_retweet_file.info(msg)
        ##logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)

        msg = f'''{"Retweeting tweets and quotes:":40}{[get_screen_name(ea) for ea in ids_to_publish_tweets_and_quotes_list]}'''
        ##logger_retweet_file.info(msg)
        ##logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)

        not_restricted_ids = [ea for ea in ids_to_follow_list]
        for ea in ids_to_publish_only_tweets_list:
            not_restricted_ids.remove(ea)

        for ea in ids_to_publish_tweets_and_quotes_list:
            not_restricted_ids.remove(ea)

        msg = f'''{"Retweeting tweets, quotes and retweets:":40}{[get_screen_name(ea) for ea in not_restricted_ids]}'''
        ##logger_retweet_file.info(msg)
        ##logger_retweet_error_file.warning(msg)
        logger_stdout.info(msg)
    

class CustomStreamingClient(tweepy.StreamingClient):
    """https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

    https://developer.twitter.com/en/docs/twitter-api/fields
    """

    def on_tweet(self, tweet):
        try:
            publish = False
            log_msg = True
            tweet_type = 'Unknown'
            logger_stdout.info(f'{tweet.text}')
            logger_retweet_file.info(f'{tweet.text}')
            logger_retweet_error_file.warning(f'{tweet.text}')

            logger_stdout.info(f'{tweet.author_id}')
            logger_retweet_file.info(f'{tweet.author_id}')
            logger_retweet_error_file.warning(f'{tweet.author_id}')

            logger_stdout.info(f'Which user_id is this a reply: {tweet.in_reply_to_user_id}')
            logger_retweet_file.info(f'Which user_id is this a reply: {tweet.in_reply_to_user_id}')
            logger_retweet_error_file.warning(f'Which user_id is this a reply: {tweet.in_reply_to_user_id}')


            if not tweet.author_id in known_users:
                known_users[tweet.author_id] = get_screen_name(tweet.author_id)

            logger_stdout.info(known_users[tweet.author_id])

####            is_retweet = hasattr(status, 'retweeted_status')
####            is_quote = status.is_quote_status
####
####
####            if status.user.id == credentials.id:
####                tweet_type = 'Apps own retweet'
####                log_msg = include_replys_and_self_retweets_in_log == "yes"
####            elif status.user.id not in ids_to_follow_list:
####                tweet_type = 'status.user.id not in ids_to_follow_list: not an account being followed'
####            elif status.in_reply_to_status_id:
####                tweet_type = 'Reply'
####                log_msg = include_replys_and_self_retweets_in_log == "yes"
####            elif not is_retweet and not is_quote:
####                tweet_type = 'Simple Tweet'
####                publish = True
####            elif not is_retweet and is_quote:
####                tweet_type = 'Simple Quote'
####                if status.user.id not in ids_to_publish_only_tweets_list:
####                    if status.quoted_status.user.id not in ids_to_follow_list: # as this should have been published already
####                        publish = True
####                    else:
####                        tweet_type = tweet_type + ' should have been retweeted already'
####                        #logger_stderr.warning(f'What #2 - {status.user.id}')
####                        #logger_stderr.warning(f'What #2 - {ids_to_follow_list}')
####                        #logger_stderr.warning(f'What #2 - {status.quoted_status.user.id}')
####            elif is_retweet:
####                tweet_type = 'Retweet'
####                if is_quote:
####                    tweet_type = tweet_type + ' with Quote'
####                # else check permissions
####                elif status.user.id not in ids_to_publish_only_tweets_list: # that is, status.id is allowed to retweet
####                    if status.user.id not in ids_to_publish_tweets_and_quotes_list: # that is, status.id is allowed to retweet
####                        if status.retweeted_status.user.id not in ids_to_follow_list: # as this should have been published already
####                            publish = True
####                            if is_quote and status.quoted_status.user.id in ids_to_follow_list: # if there is a quote in the retweet, this should have been published already
####                                publish = False
####                                tweet_type = tweet_type + ' should have been retweeted already'
####                        else:
####                            tweet_type = tweet_type + ' should have been retweeted already'
####
####            if publish:
####                if Publish_Live:
####                    r = api.retweet(status.id)
####
        except Exception as e:
            logger_stderr.warning('Custom Streaming Client error - {} - {}'.format(type(e).__name__, e))
            logger_retweet_error_file.warning('IDPrinter error - {} - {}'.format(type(e).__name__, e))
####
####        finally:
####            if log_msg:
####                msg = f'' \
####                      f'Publish_Live: {str(Publish_Live):5} | ' \
####                      f'Published: {str(publish):5} | ' \
####                      f'{tweet_type:20} | ' \
####                      f'''{status.user.screen_name:12} | ''' \
####                      f'''{status.id:12} | ''' \
####                      f'''{status.text}''' \
####                      f''
####                ##logger_retweet_file.info(msg)
####                logger_stdout.info(msg)

def get_stream_rules():
    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in ids_to_follow_list]

    return stream_rules

def main():
    try:
        # Initialize instance of the subclass
        logger_stderr.warning('Starting tweepy.Stream')
        ##logger_retweet_error_file.warning('Starting tweepy.Stream')

        check_ids_to_follow()

        streaming_client = CustomStreamingClient(bearer_token)
        streaming_client.add_rules(add=get_stream_rules())
        stream_rules = streaming_client.get_rules()
        logger_stdout.info(f'stream_rules: {stream_rules}')
        logger_retweet_file.info(f'stream_rules: {stream_rules}')
        logger_retweet_error_file.warning(f'stream_rules: {stream_rules}')
        #return streaming_client
        streaming_client.filter(expansions=['author_id'])

    
    except KeyboardInterrupt:
        streaming_client.disconnect()
        logger_stderr.warning("""
        Closing ...
        """)
        logger_stderr.warning("""
        Disconnecting streaming client ...
        """)
    except Exception as e:
        logger_stderr.error('Stream error - {} - {}'.format(type(e).__name__, e))
        logger_retweet_error_file.error('Stream error - {} - {}'.format(type(e).__name__, e))
    finally:
        streaming_client.disconnect()
        logger_stderr.warning("""
        """)
        logger_retweet_error_file.warning(f'''Disconnecting streaming client ...''')

if __name__ == '__main__':
    try:    
        main()
    except KeyboardInterrupt:
        logger_stderr.warning("""
        Closing ...
        """)

# vim: ai et ts=4 sw=4 sts=4 nu
