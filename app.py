'''
app.py will become the interface that the user interacts
with to perform analysises on collected tweets
'''

import sys
import os
import shutil
import datetime 
import math

# Custom modules
from extract import extract 
from mine import mine

def help(flags):

    print("%s\n\n> File: app.py" \
        "\n\n> Description: Mine, extract, and analyze twitter data " \
        "based on provided arguments." \
        "\n\n> Options:" \
        "\n\thelp: [%s]" \
        "\n\n\tmine: [%s]" \
        "\n\n\tremine: [%s]" \
        "\n\n\t> [re]mine options:" \
        "\n\n\t\t- username: [%s] <str>" \
        "\n\n\t\t- since: [%s] yyyy-mm-dd" \
        "\n\n\t\t- until: [%s] yyyy-mm-dd" \
        "\n\n\t\t- query search: [%s] <str>" \
        "\n\n\t\t- top tweets: [%s]" \
        "\n\n\t\t- near: [%s] <str>" \
        "\n\n\t\t- within: [%s] <int>[mi | km]" \
        "\n\n\t\t- language: [%s] <str>" \
        "\n\n\t\t- language list: [%s]" \
        "\n\n\t\t- tweet limit: [%s] <int>" \
        "\n\n\t\t- hashtags: "
        "\n\n\t\t\t- file: [%s] <file>" \
        "\n\n\t\t\t- list: [%s] \"tag, tag, ..., tag\"" \
        "\n\n\textract: [%s]" \
        "\n\n%s" % 
            ('-'*80, 
            ', '.join(flags["help"]), 
            ', '.join(flags["mine"]),
            ', '.join(flags["remine"]),
            ', '.join(flags["query"]["username"]),
            ', '.join(flags["query"]["since"]),
            ', '.join(flags["query"]["until"]),
            ', '.join(flags["query"]["query_search"]),
            ', '.join(flags["query"]["top_tweets"]),
            ', '.join(flags["query"]["near"]),
            ', '.join(flags["query"]["within"]),
            ', '.join(flags["query"]["language"]),
            ', '.join(flags["query"]["lang_list"]),
            ', '.join(flags["query"]["tweet_limit"]),
            ', '.join(flags["query"]["hashtags"]["file"]),
            ', '.join(flags["query"]["hashtags"]["list"]),
            ', '.join(flags["extract"]),
            '-'*80)
    )

    sys.exit(0)

def parser(args):

    # Flags to handle the command line args
    flags = {
        "help" : ["-h", "-help"], 
        "mine" : ["-m", "-mine"],
        "query" : {
            "username" : ["-user", "-username"],
            "since" : ["-s", "-since"],
            "until" : ["-u", "-until"],
            "query_search" : ["-q", "-query"],
            "top_tweets" : ["-t", "-top"],
            "near" : ["-n", "-near"],
            "within" : ["-w", "-within"],
            "language" : ["-lg", "-lang"],
            "lang_list" : ["-lg-l", "-lang-l"],
            "tweet_limit" : ["-l", "-limit"],
            "hashtags" : {
                "file" : ["-hf", "-hashfile"],
                "list" : ["-hl", "-hashlist"]
            }
        },
        "remine" : ["-r", "-remine"],
        "extract" : ["-e", "-extract"],
        "analyze" : []
    }

    # List of Twitter supported languages
    languages = {
        "en" : "English",
        "ar" : "Arabic", 
        "bn" : "Bengali",
        "cs" : "Czech",
        "da" : "Danish",
        "de" : "German",
        "el" : "Greek",
        "es" : "Spanish", 
        "fa" : "Persian",
        "fi" : "Finnish", 
        "fil" : "Filipino",
        "fr" : "French",
        "he" : "Hebrew",
        "hi" : "Hindi", 
        "hu" : "Hungarian",
        "id" : "Indonesian", 
        "it" : "Italian",
        "ja" : "Japan", 
        "ko" : "Korean", 
        "msa" : "Malay",
        "nl" : "Dutch",
        "no" : "Norwegian",
        "pl" : "Polish",
        "pt" : "Portuguese", 
        "ro" : "Romanian",
        "ru" : "Russian", 
        "sv" : "Swedish", 
        "th" : "Thai",
        "tr" : "Turkish", 
        "uk" : "Ukrainian",
        "ur" : "Urdu",
        "vi" : "Vietnamese",
        "zh-cn" : "Chinese (Simplified)",
        "zh-tw" : "Chinese (Traditional)"
    }

    # Invalid number of arguments
    if not args:
        print("\nERROR: Invalid number of arguments.\n")
        help(flags)

    # Help commands requested 
    elif any(flag in args for flag in flags["help"]):
        help(flags)

    # Language list requested
    elif any(flag in args for flag in flags["query"]["lang_list"]):
        # Create a table to display the options
        code_length = len(sorted(languages.keys(), key=len)[-1]) + 3
        name_length = len(sorted(languages.values(), key=len)[-1])
        row = '+' + ('-' * name_length) + '+' + ('-' * code_length) + '+'
        
        print("\n")
        print(row)
        print('|' + (' ' * 8) + "NAME" + (' ' * 9) + "|  CODE  |")
        print(row)
        for code, name in languages.items():
            name_partition = (name_length - len(name)) / 2
            code_partition = (code_length - len(code)) / 2

            # Spacing for tables
            name_left = math.floor(name_partition)
            name_right = math.ceil(name_partition)

            code_left = math.ceil(code_partition)
            code_right = math.floor(code_partition)

            print('|' + (' ' * name_left) + name + (' ' * name_right) + \
                '|' + (' ' * code_left) + code + (' ' * code_right) + '|')
            print(row)
        print("\n")

        sys.exit(0)

    # Check if the user supplied the 'mine' or 'remine' flag
    elif any(flag in args for flag in flags["mine"] + flags["remine"]):
        query = {
            "username" : None,
            "since" : None, 
            "until" : None, 
            "query_search" : None,
            "top_tweets" : False,
            "near" : None,
            "within" : None, 
            "language" : "en",
            "tweet_limit" : 1,
            "hashtags" : []
        }

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

        username = [args.index(i) for i in args if i in flags["query"]["username"]]
        since = [args.index(i) for i in args if i in flags["query"]["since"]]
        until = [args.index(i) for i in args if i in flags["query"]["until"]]
        search = [args.index(i) for i in args if i in flags["query"]["query_search"]]
        top_tweets = [args.index(i) for i in args if i in flags["query"]["top_tweets"]]
        near = [args.index(i) for i in args if i in flags["query"]["near"]]
        within = [args.index(i) for i in args if i in flags["query"]["within"]]
        language = [args.index(i) for i in args if i in flags["query"]["language"]]
        tweet_limit = [args.index(i) for i in args if i in flags["query"]["tweet_limit"]]
        hashtag_file = [args.index(i) for i in args if i in flags["query"]["hashtags"]["file"]]
        hashtag_list = [args.index(i) for i in args if i in flags["query"]["hashtags"]["list"]]
       
        # The user supplied a 'username' argument
        if len(username) > 1:
            print("ERROR: Only one 'username' argument can be supplied.")
            sys.exit(-1)
        
        elif len(username) == 1:
            index = username[0]
            try:
                query["username"] = args[index + 1] 

            except IndexError:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)

        # The user supplied a 'since' argument
        if len(since) > 1:
            print("ERROR: Only one 'since' query argument can be supplied.")
            sys.exit(-1)

        elif len(since) == 1:
            index = since[0]
            try:
                since = args[index + 1].split('-')

            except IndexError:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)

            # Verify yyyy-mm-dd format
            if len(since) != 3:
                print("ERROR: Please provide a valid date format for '%s' flag." % args[index])
                sys.exit(-1)
            
            else:
                try:
                    year, month, day = int(since[0]), int(since[1]), int(since[2])
                    datetime.date(year=year, month=month,day=day)
                    query["since"] = "%d-%s-%s" % (year, format(month, "02d"), format(day, "02d"))

                except ValueError:
                    print("ERROR: Please provide a valid date format for '%s' flag." % args[index])
                    sys.exit(-1)  

        # The user supplied an 'until' argument
        if len(until) > 1:
            print("ERROR: Only one 'until' query argument can be supplied.")
            sys.exit(-1)

        elif len(until) == 1:
            index = until[0]
            try:
                until = args[index + 1].split('-')

            except IndexError:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)

            # Verify yyyy-mm-dd format
            if len(until) != 3:
                print("ERROR: Please provide a valid date format for '%s' flag." % args[index])
                sys.exit(-1)
            
            else:
                try:
                    year, month, day = int(until[0]), int(until[1]), int(until[2])
                    datetime.date(year=year, month=month,day=day)
                    query["until"] = "%d-%s-%s" % (year, format(month, "02d"), format(day, "02d"))

                except ValueError:
                    print("ERROR: Please provide a valid date format for '%s' flag." % args[index])
                    sys.exit(-1)

        # The user supplied a 'search' query argument   
        if len(search) > 1:
            print("ERROR: Only one 'search' query argument can be supplied.")
            sys.exit(-1)

        elif len(search) == 1:
            index = search[0] 
            try:
                query["query_search"] = args[index + 1]
            
            except IndexError:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)
            
            if hashtag_file or hashtag_list:
                print("The provided 'Search' query will override the hashtag search.")

        # The user supplied a 'top tweets' argument
        if top_tweets:
            query["top_tweets"] = True

        # The user supplied a 'near' argument
        if len(near) > 1:
            print("ERROR: Only one 'near' argument can be supplied.")
            sys.exit(-1)
        
        elif len(near) == 1:
            index = near[0] 
            try:
                query["near"] = args[index + 1] 

            except:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)

            # The user supplied a 'within' argument
            if len(within) > 1:
                print("ERROR: Only one 'within' argument can be supplied.")
                sys.exit(-1)
            
            else:
                index = within[0]
                try:
                    within = args[index + 1] 
                
                except IndexError:
                    print("ERROR: Missing argument for '%s' flag." % args[index])
                    sys.exit(-1)
                
                within = within.strip()
                if len(within) < 3:
                    print("ERROR: Invalid format for '%s' flag." % args[index])
                    sys.exit(-1)

                else:
                    units = within[-2:].lower()
                    if units not in ["km", "mi"]:
                        print("ERROR: 'within' must have 'mi' or 'km' unit measurements.")
                    
                    try:
                        distance = int(float(within[:-2]))
                        query["within"] = str(distance) + units
            
                    except ValueError:
                        print("ERROR: '%s' is not a valid number." % within[:-2])
                        sys.exit(-1)


        # If the user supplied a 'language' argument
        if len(language) > 1:
            print("ERROR: Only one 'language' argument code can be supplied.")
            sys.exit(-1)
        
        elif len(language) == 1:
            index = language[0]
            try:
                code = args[index + 1].lower()

            except IndexError:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)
            
            if code not in languages.keys():
                print("ERROR: Language code '%s' is not a language supported by Twitter." % code)
                sys.exit(-1)

            else:
                query["language"] = code 

        # If the user set a tweet limit
        if len(tweet_limit) > 1:
            print("ERROR: Only one 'tweet limit' value allowed.")
            sys.exit(-1)

        elif len(tweet_limit) == 1:
            index = tweet_limit[0]
            try:
                tweet_limit = args[index + 1]
            
            except IndexError:
                print("ERROR: Missing argument for %s flag." % args[index])
                sys.exit(-1)

            try:
                query["tweet_limit"] = int(float(tweet_limit))
        
            except:
                print("ERROR: Tweet limit must be an integer.")
                sys.exit(-1)


        # The user supplied a 'hashtag file' argument
        for index in hashtag_file:
            try:
                file = args[index + 1]

            except IndexError:
                print("ERROR: Missing argument for '%s' flag." % args[index])
                sys.exit(-1)
            
            # Verify that the argument is a file.
            if os.path.isfile(file):

                # Extract the hashtags from the file 
                with open(file, mode='r', encoding=None) as hashtags:
                    hashtags = hashtags.readlines()

                    # Remove the newline character 
                    hashtags = [i.strip() for i in hashtags]

                    # Add non-duplicated values
                    query["hashtags"] = list(set(query["hashtags"]) | set(hashtags))

            else:
                print("ERROR: '%s' is not a valid file." % file)
                sys.exit(-1)

        # If the user supplied a list of hashtags
        if hashtag_list:
            for index in hashtag_list:
                try: 
                    hashtags = args[index + 1]
                    hashtags = hashtags.split(',')
                    hashtags = [i.strip() for i in hashtags]
                    query["hashtags"] = list(set(query["hashtags"]) | set(hashtags))
                
                except IndexError:
                    print("ERROR: Missing argument for %s flag." % args[index])
                    sys.exit(-1)

        # Clean up hashtags list
        hashtags = []
        for hashtag in query["hashtags"]:
            if hashtag[0] != '#':
                hashtag = '#' + hashtag
            hashtags.append(hashtag)
        query["hashtags"] = list(set(hashtags))
        
        # Verify that the user supplied hashtags or search query
        if not query["hashtags"]:
            if not query["query_search"]:
                print("ERROR: Hashtags OR query searches are required to perform this operation.")
                sys.exit(-1)

        # Perform the 'mine' operation 
        if any(flag in args for flag in flags["mine"]):
            return ["mine", query]

        # Perform the 'remine' operation
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
            return ["remine", query]

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
        mine(handler[1])
    
    elif handler[0] == "extract":
        extract()

    elif handler[0] == "analyze":
        pass      



