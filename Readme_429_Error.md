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
|Log|AWS Region|429 Error|size|python|tweepy|Elastic IP|Pretty Name|ami id|arch|GCC|AMI Description|
|---|--------|  :---:  |----|------|------|  :---:   |-----------|------|----|---|---------------|
|0|Oregon us-west-2|yes|t3.micro|3.8.10|12.4.1|yes|Ubuntu 20.04.5 LTS|ami-05b45bd47471e1710|x86_64|[GCC 9.4.0] on linux|Canonical, Ubuntu, 20.04 LTS, amd64 focal image build on 2022-01-31|
|1|Virginia us-east-1|no|t2.micro|3.7.10|12.4.1|no|Amazon Linux 2|ami-09d3b3274b6c5d4aa|x86_64|[GCC 7.3.1 20180712 (Red Hat 7.3.1-13)] on linux|Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2|
|2|Virginia us-east-1|no|t2.micro|3.7.10|12.4.1|yes|Amazon Linux 2|ami-09d3b3274b6c5d4aa|x86_64|[GCC 7.3.1 20180712 (Red Hat 7.3.1-13)] on linux|Amazon Linux 2 Kernel 5.10 AMI 2.0.20221004.0 x86_64 HVM gp2||
<!--
# vim: ai et ts=4 sw=4 sts=4 nu
-->
