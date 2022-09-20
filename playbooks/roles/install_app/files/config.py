"""
https://realpython.com/twitter-bot-python-tweepy/
"""
import tweepy
import logging
import os

from dotenv import load_dotenv
load_dotenv()

logger = logging.getLogger()

consumer_key = os.getenv("API_KEY")
consumer_secret = os.getenv("API_KEY_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

def create_api(): # API v1.1
    auth = tweepy.OAuth1UserHandler(
         consumer_key=consumer_key,
         consumer_secret=consumer_secret,
         access_token=access_token,
         access_token_secret=access_token_secret,
         wait_on_rate_limit=True)


    api = tweepy.API(auth, wait_on_rate_limit=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api

def create_client(): # API v2
    client = tweepy.Client(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
        wait_on_rate_limit=True)

    logger.info("API created")

    return client

# vim: ai et ts=4 sts=4 sw=4 nu
