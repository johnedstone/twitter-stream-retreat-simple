## Currently working in api-v2-debug branch
Note: this `main` branch is under development.  Still working out issues on `api-v2-debug` branch
## Description
This is simple example describing:
* Retweeting a list of twitter accounts into one twitter account
* Using [tweepy.Stream](https://docs.tweepy.org/en/stable/streaming.html)
* Using Twitter API v2
* Installed with an ansible playbook on an AWS ec2 instance (Debian)
    * install ansible `sudo apt upgrade && sudo apt install ansible`
    * install python3-virtualenv `sudo apt install python3-virtualenv`
    * Read ansible instructions in [playbooks/Readme_ansible.md](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks)

### Link to Streaming App python code

The files that this ansible playbook installs
that comprise the streaming app can be found in
[playbooks/roles/install_app/files/streaming_app.py](https://github.com/johnedstone/twitter-stream-retreat-simple/tree/main/playbooks/roles/install_app/files)

### Notes on Twitter identifiers API v2
* currently migrating this app to API v2, i.e under development

<!--
# vim: ai et ts=4 sw=4 sts=4 nu
-->
