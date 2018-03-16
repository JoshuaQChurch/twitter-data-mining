import json 
import os 
import pathlib 
import time 
import math
import copy 

import GetOlderTweets.got3 as got 

def hashtag_search(query):    
    # Tweet query configuration
    hashtags = query["hashtags"]
    tweet_limit = query["tweet_limit"] 
    since = query["since"]
    until = query["until"] 

    print("\nMining. Please wait...")
    start = time.time()
    for hashtag in hashtags:

        # Specify the search criteria based on the above query configuration
        # https://github.com/Jefferson-Henrique/GetOldTweets-python
        query = got.manager.TweetCriteria().setQuerySearch(hashtag)
        
        if tweet_limit >= 1: 
            query = query.setMaxTweets(tweet_limit)
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

    end = time.time()
    print("Tweets Mined: %d | Time Elapsed: ~%d second(s)" % (tweet_limit*len(hashtags), math.ceil(end-start)))

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


