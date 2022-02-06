#!/usr/bin/env python
import tweepy, os
import sys

auth = tweepy.OAuth2BearerHandler(os.getenv('Bearer_Token'))
api = tweepy.API(auth)
user = api.get_user(user_id="{}".format(sys.argv[1]))
print(user.screen_name)

# vim: ai et ts=4 sw=4 sts=4 nu
