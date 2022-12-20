import json
import logging
import os
import sys
import tweepy

from dotenv import load_dotenv

load_dotenv()
logging_file = os.getenv('LOGGING_FILE', 'debug.log')


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    filename=logging_file)

def create_list(string_list):
    return list(filter(None, [int(ea) for ea in string_list.split(',')]))

def get_stream_rules():
    stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in ids_to_follow_list]

    return stream_rules

bearer_token = os.getenv('BEARER_TOKEN')

ids_to_follow = os.getenv('IDS_TO_FOLLOW')
ids_to_follow_list = create_list(ids_to_follow)
logging.debug(ids_to_follow_list)
logging.debug(type(ids_to_follow_list))

ids_not_to_publish = os.getenv('IDS_NOT_TO_PUBLISH')
ids_not_to_publish_list = create_list(ids_to_follow)
logging.debug(ids_not_to_publish_list)
logging.debug(type(ids_not_to_publish_list))


class CustomStreamingClient(tweepy.StreamingClient):

    def on_tweet(self, tweet):
        logging.debug(f'tweet: {tweet}')

    def on_includes(self, includes):
        logging.debug(f'includes {includes}')

    def on_data(self, raw_data):
        super().on_data(raw_data)

        is_simple_tweet = False
        is_reply = False
        is_retweet = False
        is_quote = False
        publish = False

        my_data = json.loads(raw_data)
        logging.info(f'json.loads: {my_data}')

        if 'data' in my_data and 'includes' in my_data:
            logging.info(f'tweet text: {my_data["data"]["text"]}')
            logging.info(f'tweet id: {my_data["data"]["id"]}')
            for ea in my_data['includes']['users']:
                    logging.info(f'username: {ea["username"]}')

        logging.debug(int(my_data['data']['author_id']))
        logging.debug(type(int(my_data['data']['author_id'])))
        if my_data['data']['author_id'] in ids_not_to_publish:
            # publish is already False, i.e. will not publish
            logging.info('This tweet is in the list not to publish')
        elif(1 ==1):
            pass

        logging.info(f'Publish: {publish}')
            

def main():
    try:
        msg = '########## Starting tweepy.StreamClient ##########'
        logging.info(msg)

        stream_rules = get_stream_rules()
        logging.info(f'Stream rules: {stream_rules}')

        streaming_client = CustomStreamingClient(bearer_token)
        streaming_client.add_rules(add=stream_rules)  # only need to do once it appears

        current_stream_rules = streaming_client.get_rules()
        logging.info(f'Current stream rules: {stream_rules}')

        # https://twittercommunity.com/t/how-to-get-usernames-for-related-tweet-search-api/160086/4
        #streaming_client.filter(expansions=['author_id'], user_fields=['username'])
        streaming_client.filter(expansions=['author_id'])
        #streaming_client.filter()
    
    except KeyboardInterrupt:
        streaming_client.session.close()
        streaming_client.running = False
        streaming_client.on_disconnect()
        logging.warning('Keyboard Interrupt... closing')
    except Exception as e:
        msg = f'Streaming client error: {e}'
        logging.error(msg)

if __name__ == '__main__':
    try:    
        main()
    except KeyboardInterrupt:
        logging.warning("""
        Closing ...
        """)

# vim: ai et ts=4 sw=4 sts=4 nu
