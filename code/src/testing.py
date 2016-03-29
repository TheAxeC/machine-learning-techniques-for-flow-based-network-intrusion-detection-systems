
# Reading the config file
def read_config(file_name):
    import json

    try:
        with open(file_name) as data_file:
            return json.load(data_file)
    except Exception as e:
        print e
        return []

# Run a command through system
def system(data):
    import os

    for config in data:
        os.system('python main.py ' + config)
        print '\n----------------------------------------------\n',

# Run multiple different version of the IDS, in order to test the IDS
# Redirect all output to a general log file
# Use a config file containing:
#   [
#       "file1",
#       "file2"
#   ]
def main(config_file=None):
    if config_file == None:
        config_file = "testing.json"

    data = read_config(config_file)
    system(data)

import sys
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(str(sys.argv[1]))
    else:
        main()
