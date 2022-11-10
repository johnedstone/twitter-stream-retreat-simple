### This is branch == api-v2-debug
### The problem
Running the following snippet, in the `us-west-2` region on a Ubuntu t3.micro with an Elastic IP
resulted in the followin error, soon after starting the client.
```
Stream connection has errored or timed out
Stream encountered HTTP error: 429
HTTP error response text: {"title":"ConnectionException","detail":"This stream is currently at the maximum allowed connection limit.","connection_issue":"TooManyConnections","type":"https://api.twitter.com/2/problems/streaming-connection"}
```

### The code
The code as recommended by `tweepy` in this [discussion: link](https://github.com/tweepy/tweepy/discussions/1963)
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

### Comparison
|Log|AWS Region|429 Error|size|python|tweepy|Elastic IP|Pretty Name|ami id|arch|AMI Description|GCC|
|---|--------|  :---:  |----|------|------|  :---:   |-----------|------|-------|----------|---------------|
|0|Oregon us-west-2  |yes|t3.micro|3.8.10|12.4.1|yes|Ubuntu 20.04.5 LTS|ami-05b45bd47471e1710|x86_64|Canonical, Ubuntu, 20.04 LTS, amd64 focal image build on 2022-01-31|[GCC 9.4.0] on linux|
|1|Virginia us-east-1|no |t2.micro|3.7.10|12.4.1|no |Amazon Linux 2|ami-09d3b3274b6c5d4aa|x86_64|Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2|[GCC 7.3.1 20180712 (Red Hat 7.3.1-13)] on linux|
|2|Virginia us-east-1|no |t2.micro|3.7.10|12.4.1|yes|Amazon Linux 2|ami-09d3b3274b6c5d4aa|x86_64|Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2|[GCC 7.3.1 20180712 (Red Hat 7.3.1-13)] on linux|
|3|Oregon us-west-2  |yes|t2.micro|3.7.10|12.4.1|no |Amazon Linux 2|ami-0d593311db5abb72b|x86_64|Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2|[GCC 7.3.1 20180712 (Red Hat 7.3.1-13)] on linux|
|4|Virginia us-east-1|no|t2.micro|3.9.2|12.4.1|no|Debian GNU/Linux 11 (bullseye)|ami-09d3b3274b6c5d4aa|x86_64|Debian 11 (20220503-998)|[GCC 10.2.1 20210110] on linux|
|5|Ohio us-east-2|testing|t2.micro|3.9.2|12.4.1|no|Debian GNU/Linux 11 (bullseye)|ami-0c7c4e3c6b4941f0f|x86_64|Debian 11 (20220503-998)|[GCC 10.2.1 20210110] on linux|

### Logs
Command: `egrep -v 'Received keep' my_retweet/debug.log`

#### Log #0 (failure)
**Note: 429 error happens soon after the start, the time interval varies, but it's somewhat short**
```
2022-11-01 19:32:47,560 [DEBUG]: Starting new HTTPS connection (1): api.twitter.com:443
2022-11-01 19:32:47,890 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 200 None
2022-11-01 19:32:47,891 [INFO]: Stream connected
2022-11-01 19:33:07,776 [DEBUG]: Received keep-alive signal
2022-11-01 19:33:27,781 [DEBUG]: Received keep-alive signal
2022-11-01 19:33:47,791 [DEBUG]: Received keep-alive signal
2022-11-01 19:34:08,811 [ERROR]: Stream connection has errored or timed out
2022-11-01 19:34:08,816 [ERROR]: Connection error: requests.exceptions.ConnectionError: HTTPSConnectionPool(host='api.twitter.com', port=443): Read timed out.
2022-11-01 19:34:09,068 [DEBUG]: Resetting dropped connection: api.twitter.com
2022-11-01 19:34:09,208 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 429 171
2022-11-01 19:34:09,209 [ERROR]: Stream encountered HTTP error: 429
2022-11-01 19:34:09,210 [ERROR]: HTTP error response text: {"title":"ConnectionException","detail":"This stream is currently at the maximum allowed connection limit.","connection_issue":"TooManyConnections","type":"https://api.twitter.com/2/problems/streaming-connection"}
```

#### Log #1 (success)
**Note: Only one disconnect in almost 24 hours, and reconnected in < 1 sec with status code 200**

```
2022-11-07 15:07:36,193 [DEBUG]: Starting new HTTPS connection (1): api.twitter.com:443
2022-11-07 15:07:36,515 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 200 None
2022-11-07 15:07:36,516 [INFO]: Stream connected
2022-11-08 00:12:05,660 [ERROR]: Stream connection has errored or timed out
2022-11-08 00:12:05,671 [ERROR]: Connection error: requests.exceptions.ChunkedEncodingError: ("Connection broken: InvalidChunkLength(got length b'', 0 bytes read)", InvalidChunkLength(got length b'', 0 bytes read))
2022-11-08 00:12:05,673 [DEBUG]: Resetting dropped connection: api.twitter.com
2022-11-08 00:12:05,955 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 200 None
2022-11-08 00:12:05,955 [INFO]: Stream connected
2022-11-08 14:39:14,314 [INFO]: Stream disconnected (my Ctrl-C)
```

#### Log #2 (success)
**Note: no disconnects in 9+ hours**

```
2022-11-08 15:07:22,255 [DEBUG]: Starting new HTTPS connection (1): api.twitter.com:443
2022-11-08 15:07:22,561 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 200 None
2022-11-08 15:07:22,562 [INFO]: Stream connected
2022-11-09 00:40:54,207 [INFO]: Stream disconnected
```

#### Log #3 (failure)
**Note: 429 error within 18 min of starting**

```
2022-11-09 01:03:46,616 [DEBUG]: Starting new HTTPS connection (1): api.twitter.com:443
2022-11-09 01:03:46,883 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 200 None
2022-11-09 01:03:46,884 [INFO]: Stream connected
2022-11-09 01:21:07,411 [ERROR]: Stream connection has errored or timed out
2022-11-09 01:21:07,424 [ERROR]: Connection error: requests.exceptions.ChunkedEncodingError: ("Connection broken: ConnectionResetError(104, 'Connection reset by peer')", ConnectionResetError(104, 'Connection reset by peer'))
2022-11-09 01:21:07,425 [DEBUG]: Resetting dropped connection: api.twitter.com
2022-11-09 01:21:07,560 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 429 171
2022-11-09 01:21:07,561 [ERROR]: Stream encountered HTTP error: 429
2022-11-09 01:21:07,562 [ERROR]: HTTP error response text: {"title":"ConnectionException","detail":"This stream is currently at the maximum allowed connection limit.","connection_issue":"TooManyConnections","type":"https://api.twitter.com/2/problems/streaming-connection"}
2022-11-09 01:22:07,637 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 429 171
2022-11-09 01:22:07,638 [ERROR]: Stream encountered HTTP error: 429
2022-11-09 01:22:07,638 [ERROR]: HTTP error response text: {"title":"ConnectionException","detail":"This stream is currently at the maximum allowed connection limit.","connection_issue":"TooManyConnections","type":"https://api.twitter.com/2/problems/streaming-connection"}
2022-11-09 01:22:20,587 [INFO]: Stream disconnected
```

#### Log #4 (success)
**Note: no disconnects in almost 22 hours**
```
022-11-09 02:37:13,495 [DEBUG]: Starting new HTTPS connection (1): api.twitter.com:443
2022-11-09 02:37:13,751 [DEBUG]: https://api.twitter.com:443 "GET /2/tweets/search/stream HTTP/1.1" 200 None
2022-11-09 02:37:13,752 [INFO]: Stream connected
2022-11-10 00:15:15,530 [INFO]: Stream disconnected
```

<!--
# vim: ai et ts=4 sw=4 sts=4 nu
-->
