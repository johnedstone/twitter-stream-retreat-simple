### The problem
Running the following snippet, in the `us-west-2` region on a Ubuntu t3.micro with an Elastic IP
resulted in the followin error, soon after starting the client.
```
Stream connection has errored or timed out
Stream encountered HTTP error: 429
HTTP error response text: {"title":"ConnectionException","detail":"This stream is currently at the maximum allowed connection limit.","connection_issue":"TooManyConnections","type":"https://api.twitter.com/2/problems/streaming-connection"}
```

### The code
```
>>> import logging
>>> import tweepy
>>> logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(message)s', filename='debug.log')
>>> client = tweepy.StreamingClient(Bearer Token)
>>> client.filter()
```

Tweepy version == 4.12.1, i.e. `requirements.txt` file:
```
git+https://github.com/tweepy/tweepy.git
```
