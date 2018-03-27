'''
analysis.py will me a module of data analysis routines
that receive an attributes dictionary produced by reading
from a tweet's json file
'''

import extract
from collections import Counter
import functools
import pandas as pd

def run_analyses( analyses ):
    df = extract.extract_all_to_df()

    results = [ analysis( df ) for analysis in analyses ]

    return results

def tweet_word_count( df ):
    tweets = df[ "text" ]

    counts = Counter( functools.reduce( lambda x, y: x + y, [ tweet.split() for tweet in tweets ] ) )
    print( counts )

def main():
    analyses = [ tweet_word_count ]
    run_analyses( analyses )

# for testing only
if __name__ == "__main__":
    main()
