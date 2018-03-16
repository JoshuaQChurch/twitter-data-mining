'''
app.py will become the interface that the user interacts
with to perfrom analysises on collected tweets
'''

import sys
import os
import shutil
import datetime 

# Custom modules
from extract import extract 
from mine import hashtag_search

def help(flags):

    print("%s\n\n> File: app.py \n\n" \
        "> Description: Mine, extract, and analyze twitter data " \
        "based on provided args.\n\n" \
        "> Options:" \
        "\n\thelp: [%s]" \
        "\n\n\tmine: [%s]" \
        "\n\n\tquery:" \
        "\n\t\t- since: [%s] \"yyyy-mm-dd\"" \
        "\n\t\t- until: [%s] \"yyyy-mm-dd\"" \
        "\n\t\t- tweet limit: [%s] <int>" \
        "\n\n\tremine: [%s]" \
        "\n\n\textract: [%s]" \
        "\n\n\thashtags:" \
        "\n\t\t- file: [%s] <file>" \
        "\n\t\t- list: [%s] \"tag, tag, ..., tag\"" \
        "\n\n%s" % 
            ('-'*80, 
            ', '.join(flags["help"]), 
            ', '.join(flags["mine"]),
            ', '.join(flags["query"]["since"]),
            ', '.join(flags["query"]["until"]),
            ', '.join(flags["query"]["tweet_limit"]),
            ', '.join(flags["remine"]),
            ', '.join(flags["extract"]),
            ', '.join(flags["hashtags"]["file"]),
            ', '.join(flags["hashtags"]["list"]),
            '-'*80)
    )

    sys.exit(0)

def parser(args):

    # Flags to handle the command line args
    flags = {
        "help" : ["-h", "-help"], 
        "mine" : ["-m", "-mine"],
        "query" : {
            "since" : ["-s", "-since"],
            "until" : ["-u", "-until"],
            "tweet_limit" : ["-l", "-limit"]
        },
        "remine" : ["-r", "-remine"],
        "extract" : ["-e", "-extract"],
        "analyze" : [],
        "hashtags" : {
            "file" : ["-hf", "-hashfile"],
            "list" : ["-hl", "-hashlist"]
        }
    }

    # Invalid number of arguments
    if not args:
        print("\nERROR: Invalid number of arguments.\n")
        help(flags)

    # Help commands requested 
    elif any(flag in args for flag in flags["help"]):
        help(flags)

    # Check if the user supplied the 'mine' or 'remine' flag
    elif any(flag in args for flag in flags["mine"] + flags["remine"]):
        query = dict(
            tweet_limit = 1,
            since = None,
            until = None, 
            hashtags = None
        )
        hashtag_file = None 
        hashtag_list = None

        # Cannot mix the mine and extract args
        if any(flag in args for flag in flags["extract"]): 
            print("ERROR: Cannot use the mine and extract commands concurrently.")
            sys.exit(-1)

        # Cannot mix the mine and remine flag
        elif any(flag in args for flag in flags["remine"]):
            if any(flag in args for flag in flags["mine"]): 
                print("ERROR: Cannot use the mine and remine commands concurrently.")
                sys.exit(-1)

        # Cannot mix the mine and analyze args
        elif any(flag in args for flag in flags["analyze"]):
            print("ERROR: Cannot use the mine and analyze commands concurrently.")
            sys.exit(-1)

        file_indices = [args.index(i) for i in args if i in flags["hashtags"]["file"]]
        list_indices = [args.index(i) for i in args if i in flags["hashtags"]["list"]]
        since_indices = [args.index(i) for i in args if i in flags["query"]["since"]]
        until_indices = [args.index(i) for i in args if i in flags["query"]["until"]]
        limit_indices = [args.index(i) for i in args if i in flags["query"]["tweet_limit"]]

        # Cannot provide 2+ hashtag file args or 2+ hashtag list args
        if len(file_indices) > 1 or len(list_indices) > 1:
            print("ERROR: Cannot provide more than (1) hashtag file")
            sys.exit(-1)

        # If the user supplied a hashtag file 
        if file_indices:
            index = file_indices[0]
            try: 
                hashtag_file = args[index + 1]

            except IndexError:
                print("ERROR: Missing argument for %s flag." % args[index])
                sys.exit(-1)
                
            # Verify that the argument is a file.
            if os.path.isfile(hashtag_file):

                # Extract the hashtags from the file 
                with open(hashtag_file, mode='r', encoding=None) as hashtags:
                    hashtags = hashtags.readlines()

                    # Remove the newline character 
                    hashtags = [h.strip() for h in hashtags]

            else:
                print("ERROR: '%s' is not a valid file." % hashtag_file)
                sys.exit(-1)

        # If the user supplied a list of hashtags
        if list_indices:
            index = list_indices[0] 
            try:
                hashtag_list = args[index + 1].split(',')
                hashtag_list = [h.strip() for h in hashtag_list]

            except IndexError:
                print("ERROR: Missing argument for %s flag." % args[index])
                sys.exit(-1)

            tmp = []

            # Add the '#' symbol if it doesn't have one
            for hashtag in hashtag_list:
                if hashtag[0] != '#':
                    hashtag = '#'+hashtag 
                tmp.append(hashtag)
            hashtag_list = tmp[:]
            del tmp

        if since_indices:
            index = since_indices[0]
            try:
                since = args[index + 1].split('-')

            except IndexError:
                print("ERROR: Missing argument for %s flag." % args[index])
                sys.exit(-1)
        
            if len(since) != 3:
                print("ERROR: Please provide a valid date format.")
                sys.exit(-1)
            try:
                year, month, day = int(since[0]), int(since[1]), int(since[2])
                datetime.date(year=year, month=month,day=day)
            except ValueError:
                print("ERROR: Please provide a valid date format.")
                sys.exit(-1)
                
            since = '-'.join(since)
            query["since"] = since 
       
        if until_indices:
            index = until_indices[0]
            try:
                until = args[index + 1].split('-')

            except IndexError:
                print("ERROR: Missing argument for %s flag." % args[index])
                sys.exit(-1)

            if len(until) != 3:
                print("ERROR: Please provide a valid date format.")
                sys.exit(-1)
            try:
                year, month, day = int(until[0]), int(until[1]), int(until[2])
                datetime.date(year=year, month=month,day=day)
            except ValueError:
                print("ERROR: Please provide a valid date format.")
                sys.exit(-1)
            
            until = '-'.join(until)
            query["until"] = until 
                    
        if limit_indices:
            index = limit_indices[0]
            try:
                tweet_limit = args[index + 1]
            
            except IndexError:
                print("ERROR: Missing argument for %s flag." % args[index])
                sys.exit(-1)

            try:
                tweet_limit = int(tweet_limit)
        
            except:
                print("ERROR: Tweet limit must be an integer.")
                sys.exit(-1)

            query["tweet_limit"] = tweet_limit
                
        
        # If the user supplied a hashtag list 
        # and hashtag file, combine them
        if hashtag_file and hashtag_list:
            hashtags += hashtag_list
        
        # If the user supplied just a hashtag list,
        # update the hashtags variable
        elif hashtag_list and not hashtag_file:
            hashtags = hashtag_list[:]

        elif not hashtag_list and not hashtag_file:
            print("ERROR: Must provide either a hashtag file or list to mine.")
            sys.exit(-1)

        query["hashtags"] = hashtags

        if any(flag in args for flag in flags["mine"]):
            return "mine", query

        else:
            # Delete the data file
            path = os.path.join(os.getcwd(), "data")

            if os.path.isdir(path):
                if input("\nAre you sure you want to delete " \
                    "the file: '%s' [ y / n ] --> " % path).lower() == 'y':
                    shutil.rmtree(path)

                else:
                    print("Exiting...")
                    sys.exit(0)
            
            query["hashtags"] = hashtags 
            return "remine", query


    # Check if the user supplied the 'extract' flag
    elif any(flag in args for flag in flags["extract"]):

        # Cannot mix the mine and extract args
        if any(flag in args for flag in flags["mine"]): 
            print("ERROR: Cannot use the mine and extract commands concurrently.")
            sys.exit(-1)

        # Cannot mix the remine and extract args
        elif any(flag in args for flag in flags["remine"]): 
            print("ERROR: Cannot use the mine and extract commands concurrently.")
            sys.exit(-1)

        # Cannot mix the extract and analyze args
        elif any(flag in args for flag in flags["analyze"]):
            print("ERROR: Cannot use the mine and analyze commands concurrently.")
            sys.exit(-1)

        return ["extract"]

    # Check if the user supplied 'analyze' flags
    elif any(flag in args for flag in flags["analyze"]):
        print("Sorry, 'analyze' is currently unavailable.")
        sys.exit(-1)

    else:
        print("\nERROR: 'mine', 'remine', 'extract', or 'analyze'" \
                " flags required to use this program.\n")
        sys.exit(-1)
        

if __name__ == "__main__":
    
    handler = parser(sys.argv[1:])
    if handler[0] == "mine" or handler[0] == "remine":
        hashtag_search(handler[1])
    
    elif handler[0] == "extract":
        extract()

    elif handler[0] == "analyze":
        pass



