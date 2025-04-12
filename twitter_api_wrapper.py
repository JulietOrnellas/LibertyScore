import json ## Used for reading mock mentions from a .json file
import os  ## For reading environment variables (API keys etc..)
import tweepy ## Python library to access the real Twitter API



# === SWITCH BETWEEN FAKE AND REAL TWITTER ===
# If True, the bot uses fake data from mock_mentions file
# If False, the bot connects to Twitter
MOCK_MODE = True


if not MOCK_MODE:
    ##  These credential are needed to authenticate with Twitter's API
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")
    
    ## Using 0Auth 1.0a to log into Twitter's API (this is standard for posting tweets )
    auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)

    
    
# === GET MENTIONS ===
##  This function fetches tweets that mentioned this bot
##  If MOCK_MODE is True: It just load a sample list of tweets from mock_mentions.json
##  If MOCK_MODE is False: it actually asks Twitter for new mentions
def get_mentions(since_id=None):
    """
    This function will either pull fake mentions from mock_mentions file or real mentions
    from Twitter (real mode).
    """
    if MOCK_MODE:
        ## Load mentions from a local file 
        with open('mock_mentions.json', 'r') as f:
            return json.load(f)
    else:
        ## If we're using real Twitter, call the API to get mentions
        return api.mentions_timeline(since_id=since_id, tweet_mode='extended')
    
    
# === REPLY TO A TWEET ===
##  This function send a reply to a tweet
##  If MOCK_MODE is True: It just prints what it would have tweeted
##  If MOCK_MODE is False: It usees Twitter's API to post the tweet
def reply_to_tweet(username, text, in_reply_to_status_id):
    if MOCK_MODE:
        # Print out what the bot would say instead of actually tweeting
        print (f"[MOCK REPLY] @{username}: {text}")
    else:
        # This sends a real reply tweet to Twitter
        api.update_status(status=text, in_reply_to_status_id=in_reply_to_status_id)
        
            
    
