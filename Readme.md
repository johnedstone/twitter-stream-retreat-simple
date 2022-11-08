## Currently debugging 429 errors
As of Nov, 2022 using this branch to debug 429 errors

## Description
A simple example describing:
* Retweeting a list of twitter accounts into one twitter account
* Using [tweepy.Stream](https://docs.tweepy.org/en/stable/streaming.html)
* Installed with an ansible playbook on an AWS ec2 instance
    * Optional: When creating the ec2, add storage, so that it's persistent if the ec2 instance is destroyed.  Mount on `/opt/apps`.
         * [Reference to format additional storage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/add-instance-store-volumes.html)
         * [Reference to automount additional storage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html#ebs-mount-after-reboot)
    * install ansible `sudo apt upgrade && sudo apt install ansible`
    * install python3-virtualenv `sudo apt install python3-virtualenv`
    * Read ansible instructions in [playbooks/Readme_ansible.md](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks)

### Changes
* 03-Oct-2022: created branch api-v2
* 18-Sep-2022: created `tag` v1.1  
[commit b986ae55a228e4bd6f3f57ef992226d1080c7859](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/b986ae55a228e4bd6f3f57ef992226d1080c7859)  
```
Working example for Twitter API v1.1
```
* 23-Sep-2022: created a `tag` v2 (see notes on api-v2 branch above, 03-Oct-2022)
[commit 40d47848b5d457e33efda113d41daa50e76fd22e](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/40d47848b5d457e33efda113d41daa50e76fd22e)    
This tag is based on the Twitter API v2.  It's notes read as follows:
```
Working example for Twitter API v2 ....
still missing some tweets because of
Stream connection has errored or timed out
Stream encountered HTTP error: 429
HTTP error response text: {"title":"ConnectionException","detail":"This stream is currently at the maximum allowed connection limit.","connection_issue":"TooManyConnections","type":"https://api.twitter.com/2/problems/streaming-connection"}
```

### Link to Streaming App python code
The files that this ansible playbook installs
that comprise the streaming app can be found in
[playbooks/roles/install_app/files/streaming_app.py](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks/roles/install_app/files)

### Notes on Twitter identifiers API v2
* currently migrating this app to API v2

### Notes on Twitter identifiers API v1.1 (Obsolete)
* Retweet: If a user retweets a Quote, it is identified as a __retweet and a quote__
[reference](https://developer.twitter.com/en/docs/twitter-api/v1/data-dictionary/object-model/tweet)
* Quote: if a user quotes a tweet, it is identified as a __quote__ but not a __retweet__
* There are four possibilities:
```
hasattr(status, 'retweeted_status') == False and status.is_quote_status = False # Simple tweet, not a retweet, not a quote
hasattr(status, 'retweeted_status') == False and status.is_quote_status = True  # User has selected to 'Quote' not 'Retweet' a tweet
hasattr(status, 'retweeted_status') == True and status.is_quote_status = False  # User has selected to 'Retweet' not 'Quote' a tweet, and the tweet is not a Quote
hasattr(status, 'retweeted_status') == True and status.is_quote_status = True   # User has selected to 'Retweet' not 'Quote' a tweet, and the tweet is a Quote
```
* When a third party retweets a tweet of an account that this app is following, `Stream.filter(follow=ids_to_follow_list)`, this app "sees" this retweet, even though it is not a retweet of the account itself.  This app identifies this case and does not retweet it 

### Notes on systemd
* [For `systemctl --user`, not implemented here, see this reference](https://github.com/torfsen/python-systemd-tutorial)
<!--
# vim: ai et ts=4 sw=4 sts=4 nu
-->
