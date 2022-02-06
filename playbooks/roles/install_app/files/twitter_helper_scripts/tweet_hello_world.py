import sys
import tweepy

from config import create_api
api = create_api()

# Create a tweet
r = api.update_status("{}".format(sys.argv[1]))
print("response: {}".format(4))

