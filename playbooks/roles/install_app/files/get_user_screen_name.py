import tweepy, os

from dotenv import load_dotenv
load_dotenv()

def get_screen_name(user_id):  # API v2
    client = tweepy.Client(os.getenv('BEARER_TOKEN'))
    user = client.get_user(id=f'{user_id}')

    return user.data.username

# vim: ai et ts=4 sw=4 sts=4 nu
