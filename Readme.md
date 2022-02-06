
## Description
A simple example describing:
* Retweeting a list of tweet accounts into one twitter account
* Using [tweepy.Stream](https://docs.tweepy.org/en/stable/streaming.html)
* Installed on an AWS Ubuntu 20.04 ec2 instance with an ansible playbook
    * Optional: When creating instance add storage, so that it's persistent if instance is destroyed.  Mount on `/opt/apps`.
         * [Reference to format](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/add-instance-store-volumes.html)
         * [Reference to automount](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html#ebs-mount-after-reboot)
    * install ansible `sudo apt upgrade && sudo apt install ansible`
    * install python3-virtualenv `sudo apt install python3-virtualenv`

### Link to Streaming App
The files that this ansible playbook installs
that comprise the streaming app can be found in
[playbooks/roles/install_app/files](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks/roles/install_app/files)

<!--
# vim: ai et ts=4 sw=4 sts=4 nu
-->
