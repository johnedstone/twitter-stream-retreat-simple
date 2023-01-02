# Required
BEARER_TOKEN='put-bearer-token-here'

# Required, i.e ids to follow (and at least retweet tweets).  The largest set
IDS_TO_FOLLOW='1234,456,789,101112,131415'

# Optional, a subset of the above - just follow in log
IDS_NOT_TO_RETWEET_ANYTHING='1234'

# Optional, a subset of the above
IDS_TO_RETWEET_RETWEETS='456,789'

# Optional, a subset of the above
IDS_TO_REWTWEET_REPLIES=''

# Optional, a subset of the above
IDS_TO_RETWEET_QUOTES='456,789,101112'

# Optional - default: no (stdout)
LOG_TO_FILE='yes' 

# Optional - default: /tmp/debug.log
LOGGING_FILE_NAME='/path/to/logfile'

# Optional - default: 'info'
LOGLEVEL='debug'

CONSUMER_KEY='the consumer key here'
CONSUMER_SECRET='the consumer secret here'
ACCESS_TOKEN='the access token here'
ACCESS_TOKEN_SECRET='the access token secret here'

# Optional - default: /tmp/retweeted_ids
PATH_TO_RECORD_RETWEETS_ID='/tmp/retweeted_ids'

# vim: ai et ts=4 sw=4 sts=4 nu
