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

bearer_token = os.getenv('BEARER_TOKEN')

ids_to_follow_list = []
ids_to_follow = os.getenv('IDS_TO_FOLLOW')
if ids_to_follow:
    ids_to_follow_list = [int(ea) for ea in ids_to_follow.split(',')]


class CustomStreamingClient(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        try:
            logging.info(tweet)
        except Exception as e:
            msg = f'on_tweet Exception: {e}'
            logging.warning(msg)

    def get_stream_rules():
        stream_rules = [tweepy.StreamRule(value=f'from: {ea}', tag=f'{ea}', id=f'{ea}') for ea in ids_to_follow_list]

        return stream_rules

def main():
    try:
        msg = '########## Starting tweepy.StreamClient ##########'
        logging.info(msg)

        streaming_client = CustomStreamingClient(bearer_token)
        stream_rules = streaming_client.get_stream_rules()
        logging.info(f'Stream rules: {stream_rules}')
        #streaming_client.add_rules(add=stream_rules)  # only need to do once it appears

        current_stream_rules = streaming_client.get_rules()
        logging.info(f'Current stream rules: {stream_rules}')

        #streaming_client.filter(expansions=['author_id'])
        streaming_client.filter()
    
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
