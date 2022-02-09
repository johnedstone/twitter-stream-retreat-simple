
## Description
A simple example describing:
* Retweeting a list of tweet accounts into one twitter account
* Using [tweepy.Stream](https://docs.tweepy.org/en/stable/streaming.html) (version 4.5.0)
* Installed with an ansible playbook on an AWS ec2 instance (Ubuntu 20.04 LTS)
    * Optional: When creating the ec2, add storage, so that it's persistent if the ec2 instance is destroyed.  Mount on `/opt/apps`.
         * [Reference to format](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/add-instance-store-volumes.html)
         * [Reference to automount](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html#ebs-mount-after-reboot)
    * install ansible `sudo apt upgrade && sudo apt install ansible`
    * install python3-virtualenv `sudo apt install python3-virtualenv`

### Link to Streaming App
The files that this ansible playbook installs
that comprise the streaming app can be found in
[playbooks/roles/install_app/files](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks/roles/install_app/files)

### Notes on Twitter identifiers
* Retweet: If a user retweets a quote, it is identified as a __retweet and a quote__
(`hasattr(status, 'retweeted_status'`)
[reference](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet)
* Quote: if a user quotes a retweet, it is identified as a __quote__ but not a __retweet__
* There are four possibilities:
```
hasattr(status, 'retweeted_status') == False and status.is_quote_status = False # Simple tweet, not a retweet, not a quote
hasattr(status, 'retweeted_status') == False and status.is_quote_status = True  # User has selected 'Quote' not 'Retweet'
hasattr(status, 'retweeted_status') == True and status.is_quote_status = False  # User has selected 'Retweet' not 'Quote', and the retweet is not a Quote
hasattr(status, 'retweeted_status') == True and status.is_quote_status = True  # User has selected 'Retweet' not 'Quote', and the retweet is a Quote
```

<!--
# vim: ai et ts=4 sw=4 sts=4 nu
-->
