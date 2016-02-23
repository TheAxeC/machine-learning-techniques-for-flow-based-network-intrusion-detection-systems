
'''
The structure:
    config.json
        contains all information of the program
    config.py
        loads all attributes from config.json
    flow.py
        contains flow classes
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
    main.py
        main routine of the IDS
        controlled completely by the config.json file

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

def training_data_set(config, algorithm):
    print "Using data sets with malicious data."
    trainer = config.get_trainer()
    if not trainer:
        sys.exit()
    trained = False
    for d in config.get_data_sets():
        check_keys(d, "from", 0)
        check_keys(d, "file", "")
        check_keys(d, "to", -1)
        if trainer.train(algorithm, d["file"], d["from"], d['to']):
            trained = True
    if not trained:
        print "No training provided."
        sys.exit()

    save_model(config, algorithm)

##########################################################

def training(config, algorithm):
    print "Start training..."
    if config.use_model():
        try:
            directory = config.get_model_dir() + config.get_model().split(".")[0] + "/"
            print "Using stored model \"" + config.get_model() + "\" in directory \"" + directory + "\"."
            algorithm.load_file(directory + config.get_model())
        except IOError as e:
            print "Couldn't use stored model."
            training_data_set(config, algorithm)
    else:
        training_data_set(config, algorithm)

    print "Finished training."

##########################################################

def sniffing(config, algorithm):
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
        sniff = Sniffer()
        sniff.start("scapy")

        print "End sniffing."

##########################################################

def prediction(config, algorithm):
    print "Start predictions and checks..."
    from predictor import Predictor
    checker = Predictor(config.print_fails())
    checker.set_algorithm(algorithm)
    if config.is_check():
        print "Running Checks..."
        print "Used for checking the accuracy of the IDS"
        checker.runner(config.get_check_sets(), True)
        print "Checks done"
    if config.is_predict():
        print "Running predictions..."
        print "Used for IDS on files."
        checker.runner(config.get_predict_sets(), False)
        print "Predictions done"
    print "End predictions and checks."

##########################################################

def IDS(config):
    print "Intrusion Detection System enabled"
    # Load algortihm
    algorithm = config.get_algorithm()
    if not algorithm:
        sys.exit()
    print "Loaded algorithm: " + str(config.get_algorithm_name()) + "."

    # Start training
    training(config, algorithm)

    # Start prediction
    prediction(config, algorithm)

    # Start sniffing
    sniffing(config, algorithm)


##########################################################
##########################################################

def pcap_to_flow_convertor(files):
    print "Start conversion from pcap to flow..."

    print "Conversion done."

##########################################################
##########################################################

def main():
    # Read the config file
    from config import Config

    print "Starting IDS..."

    config = Config()
    if config.read_config():
        print "JSON Config file read successfully"
    else:
        sys.exit()

    if config.enabled():
        IDS(config)

    if config.flow_converter():
        pcap_to_flow_convertor(config.pcap_files())

    print "End of program."

##########################################################

import sys
if __name__ == "__main__":
    main()

##########################################################
##########################################################
