import pathlib 
import json 
import os 

if __name__ == "__main__":
    # Path to data directory
    path = os.path.join(os.getcwd(), "data")

    # List of hashtag subdirectories
    hashtags = os.listdir(path)

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

                # TODO - Write a handler after reading back 
                # in the json file(s)
                