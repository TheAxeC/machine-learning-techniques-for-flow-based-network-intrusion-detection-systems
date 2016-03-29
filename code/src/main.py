
'''
The structure:
    config.json
        contains all information of the program
    protocols.json
        contains information about protocols used for sniffing
    features.json
        contains all information used for feature extraction


    good.txt
        contains non-malicious labels


    config.py
        loads all attributes from config.json
    flow.py
        contains flow classes
    feature.py
        Changing the attributes given to a ml algorithm happens here
    loader.py
        loads different files such as:
            netflow
            pcap
    ml.py
        contains all ml algorithms
    predictor.py
        A simple predictor class to run predictions on a data sets
    sniffer.py
        Contains the packet sniffer
        Converts packets to netflow
    train.py
        contains the training set
    result.py
        File used to collect results from the predictions
    main.py
        main routine of the IDS
        controlled completely by the config.json file


    testing.py
        File to run multiple instances of the IDS
        with different config files
    testing.json
        Contains the different config files

Future:
    visualisation
    packet_analyser
'''

##########################################################
##########################################################

def save_model(config, algorithm):
    if config.store_model():
        import os

        directory = config.get_model_dir()
        if not os.path.exists(directory):
            os.makedirs(directory)

        directory = directory + config.get_model().split(".")[0] + "/"
        if not os.path.exists(directory):
            os.makedirs(directory)

        print "Saving model as " + config.get_model() + " in directory \"" + directory + "\"."
        algorithm.save(directory + config.get_model())

##########################################################

def check_keys(dic, key, val):
    if not key in dic:
        dic[key] = val

##########################################################

def training_data_set(config, algorithm, feature, good_labels):
    print "Using data sets with malicious data."
    trainer = config.get_trainer()
    if not trainer:
        sys.exit()

    print "Loaded training algorithm: " + str(config.get_trainer_name()) + "."
    trained = False
    for d in config.get_data_sets():
        check_keys(d, "from", 0)
        check_keys(d, "file", "")
        check_keys(d, "to", -1)
        if trainer.train(algorithm, d["file"], d["from"], d['to'], feature, good_labels):
            trained = True
    if not trained:
        print "No training provided."
        sys.exit()

    save_model(config, algorithm)

##########################################################

def training(config, algorithm, feature, good_labels):
    print "Start training..."
    if config.use_model():
        try:
            directory = config.get_model_dir() + config.get_model().split(".")[0] + "/"
            print "Using stored model \"" + config.get_model() + "\" in directory \"" + directory + "\"."
            algorithm.load_file(directory + config.get_model())
        except IOError as e:
            print "Couldn't use stored model."
            training_data_set(config, algorithm, feature, good_labels)
    else:
        training_data_set(config, algorithm, feature, good_labels)

    print "Finished training.\n"

##########################################################

def sniffing(config, algorithm, feature):
    if config.sniffer_active():
        print "Start sniffing..."

        prevention = config.prevention_active()
        if prevention:
            print "Activating Intrusion Prevention System."

        print "implement continuous monitoring"
        print "This means:"
        print "\t capturing packets"
        print "\t converting to netflow"
        print "\t analyse closed flow"

        from sniffer import Sniffer
        sniff = Sniffer(config.get_protocol_file(), config.get_flow_timeout(), feature)
        sniff.sniff_tshark(algorithm)

        print "End sniffing.\n"

##########################################################

def prediction(config, algorithm, feature, logger, good_labels):
    print "Start predictions and checks..."
    from predictor import Predictor
    checker = Predictor(config.print_fails())
    checker.set_algorithm(algorithm)
    checker.set_feature(feature)
    checker.set_logger(logger)

    from result import ResultManager
    checker.set_resultmanager(ResultManager(logger, good_labels))

    if config.is_check():
        print "Running Checks..."
        print "Used for checking the accuracy of the IDS"
        checker.runner(config.get_check_sets(), good_labels)
        print "Checks done"
    print "End predictions and checks.\n"

##########################################################

# load labels:
def load_labels(file_name):
    labels = []
    try:
        with open(file_name) as f:
            for line in f:
                labels.append(line.strip())
    except Exception as e:
        print "Could not open label file: \"" + file_name + "\"."
        return []
    return labels

##########################################################

# Set the logging files:
def start(log, good_label):
    from logger import Logger
    logger = Logger()
    logger.start(log)
    good_labels = load_labels(good_label)
    return logger, good_labels

##########################################################

def stop(logger):
    if logger:
        logger.close()

##########################################################

def load_algorithm(config):
    # Load algortihm
    algorithm = config.get_algorithm()
    if not algorithm:
        sys.exit()
    print "Loaded algorithm: " + str(config.get_algorithm_name()) + "."
    print ""
    return algorithm

##########################################################

def load_feature(config):
    feature = config.get_feature()
    if not feature:
        print "No feature loaded"
        sys.exit()
    print "Loaded feature: " + str(config.get_feature_name()) + "."
    print ""
    return feature

##########################################################

# The IDS consists of multiple parts:
#     The machine learning algorithm
#     The logger
#     The feature extraction class
#     The training suite
#         A training class
#         A model saver
#         A loader class to load files
#     A prediction suite
#         A loader class to load files
#         The predictor class
#         A class to collect the results
#     The sniffer class
#
# There are several general purpose classes that can be used:
# These are the loading classes
#     A netflow file loader
#     A SQL loader
# These components can easily be exchanged with others
# Most of these components can be set using the config file
def IDS(config):
    print "Intrusion Detection System enabled"

    # Load the algorithm that is used in the IDS
    algorithm = load_algorithm(config)

    # Load the logger
    # Should there be multiple labels
    # The good labels file denotes which labels form the non-malicious class
    logger, good_labels = start(config.get_logger_file(),
                                config.get_good_labels_file())

    # Feature is the class responsible for parsing flow record
    # These records need to be parsed into an array that can be fed
    # to a machine learning algorithm
    feature = load_feature(config)

    # Start training
    # This phase cannot be avoided or stopped
    training(config, algorithm, feature, good_labels)

    # Start prediction
    # Prediction testing phase
    # Uses pre-prepared data sets
    # Can use checkers to detect accuracy
    # And can use prediction mode, for unlabeled data
    prediction(config, algorithm, feature, logger, good_labels)

    # Start sniffing
    # Main component of the IDS
    sniffing(config, algorithm, feature)

    # Stop the logging
    stop(logger)

##########################################################
##########################################################

def pcap_to_flow_convertor(config):
    print "Start conversion from pcap to flow..."

    from sniffer import Sniffer
    sniff = Sniffer(config.get_protocol_file(), config.get_flow_timeout())

    files = config.pcap_files()
    for f in files:
        sniff.convert_flow(f['src'], f['dest'])

    print "Conversion done."

##########################################################
##########################################################

def print_labels(files):
    from loader import NetflowLoader
    loader = NetflowLoader()

    for f in files:
        check_keys(f, "file", "")
        print "Dataset: \"" + f['file'] + "\""
        print "The labels used are: "
        labels = loader.get_labels(f['file'])
        for lab in labels:
            print "\t " + lab
        print ""
    print "Done checking labels\n"

##########################################################
##########################################################

def main(config_file=None):
    # Read the config file
    from config import Config

    print "Starting IDS..."

    # Read the main config file
    config = Config(config_file)
    if config.read_config():
        print "JSON Config file read successfully\n"
    else:
        sys.exit()

    # Print the labels from the given datasets
    # Used to manually check which labels exist
    if config.print_labels():
        print_labels(config.get_data_sets())

    # Run the actual IDS
    if config.enabled():
        IDS(config)

    # Convert pcap files to flow files
    # These files are not labeled
    # In other words, they cannot be used for training
    # Unless they solely consist of normal or malicious behaviour
    if config.flow_converter():
        pcap_to_flow_convertor(config)

    print "End of program."

##########################################################

import sys
if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(str(sys.argv[1]))
    else:
        main()

##########################################################
##########################################################
