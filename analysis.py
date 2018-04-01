'''
analysis.py will me a module of data analysis routines
that receive an attributes dictionary produced by reading
from a tweet's json file
'''

import extract
from collections import Counter
import functools
import pandas as pd

def word_count( string ):
    return Counter( string.split() )

def concat_word_counters( a, b ):
    return a + b

def hashtag_word_count( series ):
    hashtags = series.hashtags
    string = ''.join( hashtags ) 

    return word_count( string )

def mention_word_count( series ):
    mentions = series.mentions
    string = ''.join( mentions )

    return word_count( string )

def tweet_word_count( series ):
    tweets = series.text

    return word_count( tweets )

def _apply_single_analysis( df, analysis ):
    return [ analysis( df.loc[i] ) for i in range( df.shape[0] ) ]

def apply_analyses( df, analyses ):
    if type( analyses ) is not list or len( analyses ) == 1:
        # return a list of a list for consistency
        return [ _apply_single_analysis( df, analyses ) ]

    return [ _apply_single_analysis( df, analysis ) for analysis in analyses ]

def use_case():
    df = extract.extract_all_to_df()

    analyses = [ tweet_word_count, mention_word_count, hashtag_word_count ]
    results = apply_analyses( df, analyses )
    reduction = [ sum( counter_list, Counter() ) for counter_list in results ]

    for result in reduction:
        print( result.most_common( 5 ) )

    return reduction

if __name__ == "__main__":
    use_case()
