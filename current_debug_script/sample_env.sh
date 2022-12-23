# Required
BEARER_TOKEN='put-bearer-token-here'

# Required, i.e ids to follow and retweet
IDS_TO_RETWEET_TWEETS='1234,456,789,101112,131415'

# Optional, a subset of the above - just follow in log
IDS_NOT_TO_RETWEET_ANYTHING='1234'

# Optional, a subset of the above
IDS_TO_RETWEET_RETWEETS='456'

# Optional, a subset of the above
IDS_TO_REWTWEET_REPLIES='789,101113'

# Optional, a subset of the above
IDS_TO_RETWEET_QUOTES='131415'

# Optional - default: no (stdout)
LOG_TO_FILE='yes' 

# Optional - default: 'info'
LOGLEVEL='debug'
