
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

def training(config, algorithm):
    print "Start training..."
    if config.use_model():
        print "Using stored model."
        algorithm.load_file(config.get_model())
    else:
        print "Using data sets with malicious data."
        trainer = config.get_trainer()
        if not trainer:
            sys.exit()
        for d in config.get_data_sets():
            trainer.train(algorithm, d["file"], d["from"], d['to'])
        print "Saving model as " + config.get_model() + "."
        algorithm.save(config.get_model())
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
    import sys

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

if __name__ == "__main__":
    main()

##########################################################
##########################################################
