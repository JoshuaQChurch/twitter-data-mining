import pathlib 
import json 
import os 
import pandas as pd

def get_hashtags( path=os.getcwd() ):
    path = os.path.join( path, "data" )

    if not os.path.isdir( path ):
        return []

    hashtags = os.listdir( path )
            
    if ".DS_Store" in hashtags:
        hashtags.remove(".DS_Store")

    # strip the '#' character
    return [ tag[1:] for tag in hashtags ]

def extract_tweets_to_df( hashtag, path=os.getcwd() ):
    hashtags = get_hashtags( path ) 

    if hashtag.startswith( '#' ):
        hashtag = hashtag[1:]

    if hashtag not in hashtags:
        raise ValueError( "Hashtag '#" + hashtag + "' has not been mined" )

    # Path to data directory
    path = os.path.join( path, "data" )

    tweets = []

    if os.path.isdir(path):
        files = os.listdir( os.path.join( path, '#' + hashtag ) )

        for fh in files:
            # The file within the subdirectory
            filename = os.path.join( path, '#' + hashtag, fh )

            # Open the file and extract the dict()
            with open( filename, 'r' ) as f:
                attributes = json.load(f)
                tweets.append( attributes )

    return pd.DataFrame( tweets )

def extract_all_to_df():
    hashtags = get_hashtags()

    if not hashtags:
        raise ValueError( "No hashtags found. Have you mined any tweets yet?" )

    frames = [ extract_tweets_to_df( tag ) for tag in hashtags ]

    # we could instead return the list of data frames
    return pd.concat( frames )

def extract(path=os.getcwd()):
    # Path to data directory
    path = os.path.join(path, "data")

    if os.path.isdir(path):
        if not input("\nAre you sure you want to extract the values from " \
                "the this path? '%s' [ y / n ] --> " % path).lower() == 'y':

            exit()

        # List of hashtag subdirectories
        hashtags = os.listdir(path)

        if hashtags:

            # Remove .DS_Store from the list
            if ".DS_Store" in hashtags:
                hashtags.remove(".DS_Store")
            
            for tag in hashtags:
                # List of files within each sub directory
                files = os.listdir(os.path.join(path, tag))

                for file in files:
                    # The file within the subdirectory
                    filename = os.path.join(path, tag, file)

                    # Open the file and extract the dict()
                    with open(filename, 'r') as f:
                        attributes = json.load(f)
                        print(attributes)
                        # TODO: Write handler for this. 
                        exit()
    else:
        print("You must mine data before extracting.")
        exit()

                
