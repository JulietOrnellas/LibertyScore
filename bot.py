import tweepy
import time  ## Allows me to pause the bot so it doesn't run constnantly
import os   ## Helps me work with environment variaples - api keys, etc...
#import requests  # lets me make http requests to get the liberty score page
#from bs4 import BeautifulSoup ## used to scrape infrom from webpage

from dotenv import load_dotenv

## Import my own wrapper to handle either real or mock testing
from twitter_api_wrapper import get_mentions, reply_to_tweet
load_dotenv()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 



API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Tweepy Client
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

# Keep track of last seen mention ID, ie the last tweet we replied to
LAST_SEEN_FILE = 'last_seen.txt'

## This function reads the last tweet ID from a local file so we don't reply
## to the same tweet over and over
# Twitter mentions are returned in order from newest to oldest, so we use this 
## to track the most recent one we handled.


def get_last_seen_id():
    try:
        with open(LAST_SEEN_FILE, 'r') as f:
            return int(f.read().strip())  ## return the id as an integer
    except:
        return None    ## if file doesn't exit yet, we haven't seen any tweets
    
    
## This function write the ID of the most recent tweet we've responded to
## We update this everyt time we reply to a new mention   
def set_last_seen_id(tweet_id):
    with open(LAST_SEEN_FILE, 'w') as f:
        f.write(str(tweet_id))
        
# Extract name by removing bot handle
## takes full tweet text and removes the bot handle
def extract_name(tweet_text, bot_handle="@LibertyLookup"):
    return tweet_text.replace(bot_handle,"").strip().lower()
    
## This function looks up the liberty score from the website.  It takes the name
## and tries to load the relevant page
## Then it scrapes the page to find the score (it's stored in a <div> with class="score-card-score")
# Liberty Score parser
def get_liberty_score(name):
    ##  Converts politicians name into a url to look up
    url = f"https://libertyscore.conservativereview.com/{name.lower().replace(' ', '-')}"
    
    service = Service(executable_path="./chromedriver.exe")
    options = webdriver.ChromeOptions() 
    options.add_argument('--headless') # optional, no browser window
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get(url)
        time.sleep(3)   ## gives a few seconds to load the page
        
        # Try to locate the score element
        score_element = driver.find_element(By.CLASS_NAME, "scorePercent")
        return score_element.text.strip()  
    
    except Exception as e:
        print ("Error getting score:", e)   
        return "Could not retrieve Liberty Score"
    
    finally:
        driver.quit()
   



# === This is the core function that does all the work:
# 1. Checks for new mentions
# 2. Extracts the name
# 3. Finds their Liberty Score
# 4. Replies to the tweet with the score

def check_mentions():
    print ("Checking mentions...")
    ## This loads the ID of the last tweet we responded to
    last_seen_id = get_last_seen_id()
    
    # This fetches all the tweets that mention @LibertyLookup since that last tweet
    # Twitter returns each "mention" as a dictionary, containing:
    # - 'id': the tweet's unique ID number
    # - 'user': info about the person who tweeted, including 'screen_name'
    # - 'text' or 'full_text': the actual tweet message
    
    mentions = get_mentions(since_id=last_seen_id)
    
    # Reverse the mentions because Twitter gives them from newest to oldest
    # But we want to reply to the OLDEST first so replies stay in order
    for mention in reversed(mentions):
        ##  Get the tweet's message
        tweet_text = mention.get('full_text') or mention.get('text') 
         
        print (f"Found mention from @{mention['user']['screen_name']}: {tweet_text}")
                
        ## Extract the politician's name from the tweet
        name = extract_name(tweet_text)
        
        ##  Find the Liberty Score for that name
        score = get_liberty_score(name) 
        
        ## format the reply- tagging the original user and the score
        reply= f"@{mention['user']['screen_name']} Liberty Score for '{name.title()}': {score}"
        
        ## Post the reply using the Twitter wrapper (either real or fake)
        reply_to_tweet(mention['user']['screen_name'], reply, mention['id'])
        
        print(f"Replied with: {reply}")
        
        ## Save the last seen ID for later (but do not write it yet)
        last_mention_id = mention['id']
        
# Loop every 60 seconds
while True:
    check_mentions() 
    time.sleep(60)
    

