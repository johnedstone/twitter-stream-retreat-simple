import json
import logging
import os
import sys
import tweepy

from dotenv import load_dotenv

load_dotenv()
print_to_file = os.getenv('PRINT_TO_FILE', 'no') == 'yes'
logging_file = os.getenv('LOGGING_FILE', 'debug.log')


if print_to_file:
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s]: %(message)s', filename=logging_file)
else:
    logging.basicConfig(level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s]: %(message)s')

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
        logging.debug(f'{"#"*20} Start {"#"*20}') 
        logging.debug(f'tweet: {tweet}')
        logging.debug(f'tweet.data: {tweet.data}')
        logging.debug(f'tweet.author_id: {tweet.author_id}')
        logging.debug(f'tweet.in_reply_to_user_id: {tweet.in_reply_to_user_id}')
        logging.debug(f'tweet.referenced_tweets: {tweet.referenced_tweets}')
        logging.debug(f'{dir(tweet)}')

        if int(tweet.author_id) in ids_not_to_publish_list:
            logging.debug('This tweet is in the list not to publish')

        if tweet.in_reply_to_user_id:
            logging.debug('This tweet is a reply')
        else:
            logging.debug('This tweet is NOT a reply')

        if 'referenced_tweets' in tweet.data.keys():
            for ea in tweet.data['referenced_tweets']:
                if ea['type'] == 'quoted':
                    logging.debug('This is a quote')
                if ea['type'] == 'retweeted':
                    logging.debug('This is a retweet')
        else:
            logging.debug('This is a simple tweet, i.e. not a Reply, Retweet, nor Comment ("Quoted Tweet")')
        
        logging.debug(f'{"#"*20} END {"#"*20}') 

    def on_includes(self, includes):
        logging.debug(f'includes {includes}')

    def on_data(self, raw_data):
        super().on_data(raw_data)

        my_data = json.loads(raw_data)
        logging.debug(f'json.loads: {my_data}')
            

def main():
    try:
        msg = '########## Starting tweepy.StreamClient ##########'
        logging.info(msg)

        stream_rules = get_stream_rules()
        logging.info(f'Stream rules: {stream_rules}')

        streaming_client = CustomStreamingClient(bearer_token)
        streaming_client.add_rules(add=stream_rules)  # only need to do once it appears, but no harm in calling it

        current_stream_rules = streaming_client.get_rules()
        logging.info(f'Current stream rules: {stream_rules}')

        streaming_client.filter(expansions=['author_id'], user_fields=['username'],
                tweet_fields=['in_reply_to_user_id', 'referenced_tweets'])
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
