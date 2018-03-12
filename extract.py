import pathlib 
import json 
import os 

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

                