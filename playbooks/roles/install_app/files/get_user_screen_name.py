import tweepy, os

from dotenv import load_dotenv
load_dotenv()

def get_screen_name(user_id):
    auth = tweepy.OAuth2BearerHandler(os.getenv('BEARER_TOKEN'))
    api = tweepy.API(auth)
    user = api.get_user(user_id=f'{user_id}')

    return user.screen_name

# vim: ai et ts=4 sw=4 sts=4 nu
