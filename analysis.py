'''
analysis.py will me a module of data analysis routines
that receive an attributes dictionary produced by reading
from a tweet's json file
'''

# Disclaimer: Nothing works yet, <3 wil

import extract
from collections import Counter
import functools
import pandas as pd

def run_analyses( analyses ):
    df = extract.extract_all_to_df()

    # results = [ analysis( tweet ) for analysis in analyses ]

    master = []

    for tweet in df:
        results = [ analysis( tweet ) for analysis in analyses ]
        master.append( results )
        results = []

    return master

def word_count( string ):
    return Counter( string.split() )

def concat_word_counters( a, b ):
    return a.update( b )

def apply_to_all( df, function ):
    return [ function( tweet ) for tweet in df ]

def hashtag_word_count( tweet ):
    hashtags = tweet[ "hashtags" ]
    string = ''.join( hashtags ) 

    return word_count( string )

def mention_word_count( tweet ):
    mentions = tweet[ "mentions" ]
    string = ''.join( mentions )

    return word_count( string )

def tweet_word_count( tweet ):
    tweets = tweet[ "text" ]

    # counts = Counter( functools.reduce( lambda x, y: x + y, [ tweet.split() for tweet in tweets ] ) )
    # return counts

    return word_count( tweets )

def old_main():
    analyses = [ tweet_word_count ]
    run_analyses( analyses )

def main():
    df = extract.extract_all_to_df()

    counters = [ tweet_word_count( df.loc[i] ) for tweet in df.iterrows() ]
    counts = functools.reduce( concat_word_counts, counters )

    print( counts.most_common( 5 ) )

def iterate():
    df = extract.extract_all_to_df()

    for tweet in df.iterrows():
        print( type( tweet ) )

# for testing only
if __name__ == "__main__":
    # main()
    iterate()
