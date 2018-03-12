import json 
import os 
import pathlib 
import time 
import math
import copy 

import GetOlderTweets.got3 as got 

def hashtag_search(query):
    keys = list(query.keys())
    
    # Tweet query configuration
    hashtags = query["hashtags"]
    tweet_limit = 1000
    if "tweet_limit" in keys: 
        tweet_limit = query["tweet_limit"]

    original_tweet_limit = copy.deepcopy(tweet_limit)

    tweets_per_hashtag = math.ceil(tweet_limit / len(hashtags))
    since = None 
    if "since" in keys:
        since = query["since"]   # YYYY-MM-DD
    
    until = None 
    if "until" in keys:
        until = query["until"]    # YYYY-MM-DD

    modulo = len(hashtags) - 1
    if modulo == 0:
        modulo = 1

    # Counter to handle modulo operator
    # for switching between each hashtag 
    i = 0
    print("\nMining. Please wait...")
    start = time.time()
    while tweet_limit > 0: 
        # Alternate through the list of hashtags
        # to get to balance the tweet requests
        hashtag = hashtags[i % modulo]

        # Specify the search criteria based on the above query configuration
        # https://github.com/Jefferson-Henrique/GetOldTweets-python
        query = got.manager.TweetCriteria().setQuerySearch(hashtag).setMaxTweets(tweets_per_hashtag)
        if since:
            query = query.setSince(since)
        if until:
            query = query.setUntil(until)

        tweets = got.manager.TweetManager.getTweets(query)
        
        for tweet in tweets:
            attributes = dict(
                permalink = tweet.permalink, 
                username = tweet.username, 
                text = tweet.text, 
                date = str(tweet.date),
                retweets = tweet.retweets, 
                favorites = tweet.favorites, 
                mentions = tweet.mentions, 
                hashtags = tweet.hashtags.split(' '),
                geo = tweet.geo
            )

            # Store results in a file
            write_to_file(attributes, hashtag, tweet.id)

        # Deduct the results from the max 
        tweet_limit -= len(tweets)

        i += 1
    
    end = time.time()
    print("Tweets Mined: %d | Time Elapsed: ~%d second(s)" % (original_tweet_limit, end-start))

# Write the tweet dictionary to a persistent file                                 
def write_to_file(attributes, hashtag, id):
    # Path to the sub folder 
    path = os.path.join(os.getcwd(), "data", hashtag)

    # Create the folder if it does not exist
    pathlib.Path(path).mkdir(parents=True, exist_ok=True) 

    # Path to the file in the sub folder 
    file = os.path.join(path, id)

    # Create the file and write the data
    with open(file, 'w+') as f:
        json.dump(attributes, f)


