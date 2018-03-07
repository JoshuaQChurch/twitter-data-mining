import json 
import os 

import tweepy
from tweepy import OAuthHandler
from tweepy import TweepError

def hashtag_search(hashtags, api):
    # List to store tweet results 
    tweets = []
    for tag in hashtags:
        # Maximum number of results to get for each hashtag
        result_count = 1
        results = api.search(tag, rpp=result_count)
        if results:
            tweets.append(results)   

    return tweets 


if __name__ == "__main__":
    # List of files in the current working directory 
    files = os.listdir(os.getcwd())

    # Verify the user has the credentials to use the app 
    if "credentials.json" not in files:
        print("Please provide your credentials file before continuing.")
        exit(-1)

    # Verify that the user has supplied a list of hashtags
    # to search for. 
    if "hashtags" not in files:
        print("Please provide a hashtags file before continuing.")
        exit(-1)
    
    # Extract the credentials
    credentials = json.load(open("credentials.json"))
    consumer_key = credentials["consumer_key"]
    consumer_secret = credentials["consumer_secret"]
    access_token = credentials["access_token"]
    access_secret = credentials["access_secret"]

    # Authorize through OAuth
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    # Create the API object 
    api = tweepy.API(auth)

    # Verify that the authorization process was accepted
    try:
        api.me()

    except TweepError:
        print("Unable to authenticate your credentials. Please verify " \
            "that your credentials are correct and try again.")
        exit(-1)

    # Extract the hashtags from the file 
    with open("hashtags", mode='r', encoding=None) as hashtags:
        hashtags = hashtags.readlines()

        # Remove the newline character 
        hashtags = [h.strip() for h in hashtags] 

    results = hashtag_search(hashtags, api)

