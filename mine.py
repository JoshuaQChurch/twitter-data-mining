import json 
import os 
import pathlib 
import time 
import math

import GetOlderTweets.got3 as got 

def hashtag_search(hashtags):
    # Tweet query configuration 
    total_tweet_limit = 1000
    max_tweets = math.ceil(total_tweet_limit / len(hashtags))
    start_date = "2018-01-07"   # YYYY-MM-DD
    end_date = "2018-01-08"     # YYYY-MM-DD

    # Counter to handle modulo operator
    # for switching between each hashtag 
    i = 0
    while total_tweet_limit > 0: 
        # Alternate through the list of hashtags
        # to get to balance the tweet requests
        hashtag = hashtags[i % (len(hashtags) - 1)]

        # Specify the search criteria based on the above query configuration
        # https://github.com/Jefferson-Henrique/GetOldTweets-python
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(hashtag).setSince(start_date).setUntil(end_date).setMaxTweets(max_tweets)
        tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        
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
        total_tweet_limit -= len(tweets)

        i += 1


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


if __name__ == "__main__":
    # List of files in the current working directory 
    files = os.listdir(os.getcwd())

    # Verify that the user has supplied a list of hashtags
    # to search for. 
    if "hashtags" not in files:
        print("Please provide a hashtags file before continuing.")
        exit(-1)

    # Extract the hashtags from the file 
    with open("hashtags", mode='r', encoding=None) as hashtags:
        hashtags = hashtags.readlines()

        # Remove the newline character 
        hashtags = [h.strip() for h in hashtags] 

    # Search for each hashtag and collect the data
    hashtag_search(hashtags)

