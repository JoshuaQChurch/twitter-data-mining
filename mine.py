import json 
import os 
import pathlib 
import time 
import math
import copy 

import GetOlderTweets.got3 as got 


def set_query(query):
    # Tweet query configuration
    username = query["username"]
    since = query["since"]
    until = query["until"] 
    top_tweets = query["top_tweets"] 
    near = query["near"]
    within = query["within"]
    language = query["language"]
    tweet_limit = query["tweet_limit"]

    tweet_query = got.manager.TweetCriteria().setTopTweets(top_tweets)

    if username:
        tweet_query = tweet_query.setUsername(username)
    
    if since:
        tweet_query = tweet_query.setSince(since)

    if until:
        tweet_query = tweet_query.setUntil(until)
    
    """
    # Set near and within are not working with Python 3 currently.
    if near:
        print("near")
        tweet_query = tweet_query.setNear(near)

    if within:
        print("within")
        tweet_query = tweet_query.setWithin(within)
    """

    if language:
        tweet_query = tweet_query.setLang(language)

    if tweet_limit >= 1:
        tweet_query = tweet_query.setMaxTweets(tweet_limit)

    return tweet_query 


def mine(query):    
    # Tweet query configuration
    print("\nMining. Please wait...")
    start = time.time()

    tweet_query = set_query(query)
    tweet_count = 0

    if query["query_search"]:
        scale = 1
        tweet_query = tweet_query.setQuerySearch(query["query_search"])
        tweets = got.manager.TweetManager.getTweets(tweet_query)
        
        for tweet in tweets:
            tweet_count += 1
            attributes = dict(
                permalink = tweet.permalink, 
                username = tweet.username, 
                text = tweet.text, 
                date = str(tweet.date),
                retweets = tweet.retweets, 
                favorites = tweet.favorites, 
                mentions = tweet.mentions.split(' '), 
                hashtags = tweet.hashtags.split(' '),
                geo = tweet.geo
            )

            # Store results in a file
            write_to_file(attributes, "Search-Query", tweet.id)

    else:
        scale = len(query["hashtags"])
        for hashtag in query["hashtags"]:

            # Specify the search criteria based on the above query configuration
            # https://github.com/Jefferson-Henrique/GetOldTweets-python
            tweet_query = tweet_query.setQuerySearch(hashtag)
            tweets = got.manager.TweetManager.getTweets(tweet_query)
            
            for tweet in tweets:
                tweet_count += 1
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
    
    if query["tweet_limit"] >= 1:
        expected = str(query["tweet_limit"] * scale) 
    else:
        expected = "No Limit."

    print("Expected Tweets Mined: %s | Actual Tweets Mined: %d | Time Elapsed: ~%d second(s)" % 
        (expected, tweet_count, math.ceil(end-start)))



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


