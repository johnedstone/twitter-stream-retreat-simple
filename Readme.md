
## Description
A simple example describing:
* Retweeting a list of twitter accounts into one twitter account
* Using [tweepy.Stream](https://docs.tweepy.org/en/stable/streaming.html) (version 4.5.0)
* Installed with an ansible playbook on an AWS ec2 instance (Ubuntu 20.04 LTS)
    * Optional: When creating the ec2, add storage, so that it's persistent if the ec2 instance is destroyed.  Mount on `/opt/apps`.
         * [Reference to format additional storage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/add-instance-store-volumes.html)
         * [Reference to automount additional storage](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html#ebs-mount-after-reboot)
    * install ansible `sudo apt upgrade && sudo apt install ansible`
    * install python3-virtualenv `sudo apt install python3-virtualenv`
    * Read ansible instructions in [playbooks/Readme_ansible.md](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks)

### Link to Streaming App python code
The files that this ansible playbook installs
that comprise the streaming app can be found in
[playbooks/roles/install_app/files/streaming_app.py](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks/roles/install_app/files)

### Notes on Twitter identifiers API v2
* currently migrating this app to API v2

### Notes on Twitter identifiers API v1.1
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
