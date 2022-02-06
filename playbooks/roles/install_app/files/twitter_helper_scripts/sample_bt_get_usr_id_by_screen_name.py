#!/usr/bin/env python
import tweepy, os
import sys

from dotenv import load_dotenv
load_dotenv('../.env')

auth = tweepy.OAuth2BearerHandler(os.getenv('BEARER_TOKEN'))
api = tweepy.API(auth)
user = api.get_user(screen_name="{}".format(sys.argv[1]))
print(user.id)

# vim: ai et ts=4 sw=4 sts=4 nu
