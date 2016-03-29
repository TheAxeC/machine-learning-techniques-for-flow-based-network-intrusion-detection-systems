
# A predictor class
class Predictor:

    # Initialisation of variables
    def __init__(self, print_total=False):
        self.totals = 0

        self.start = 0
        self.finish = 0

        self.algorithm = None
        self.feature = None
        self.minimize = not print_total

    # Set the result class
    def set_resultmanager(self, result):
        self.results = result

    # Set the feature class
    def set_feature(self, feature):
        self.feature = feature

    # Set the algorithm class
    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def set_logger(self, logger):
        self.logger = logger

    # Run the predictor
    def runner(self, data_set, good_labels):
        for d in data_set:
            self.check_keys(d, "from", 0)
            self.check_keys(d, "file", "")
            self.check_keys(d, "to", -1)
            print "Start file: " + str(d['file']) + "."
            try:
                self.predict_file(d, good_labels)
            except KeyboardInterrupt as e:
                self.logger.update_progress(-1)
                print "KeyboardInterrupt occured..."
            print "End file: " + str(d['file']) + "."
        print self.results.get_output()

    # Check whether the key exists
    def check_keys(self, dic, key, val):
        if not key in dic:
            dic[key] = val

    # Predict the elements in a file
    def predict_file(self, d, good_labels):
        from loader import NetflowLoader
        loader = NetflowLoader()
        if not loader.load(d['file'], d['from'], d['to'], None, False):
            print "Dataset \"" + d['file'] + "\" could not be loaded."
            return False

        samples = loader.get_netflow()
        print "Start predicting..."
        self.predict(samples)

    # Predict a single flow file that has been loaded
    def predict(self, flow):
        if self.algorithm:
            self.loop(flow)
        else:
            print "Please set an algorithm first."

    def loop(self, netflow):
        i = 0

        size = netflow.get_size()
        while i < size:
            flow = netflow.get_sample_data(self.feature)[i]
            label =  netflow.get_target_data()[i]
            result = self.algorithm.predict(flow, label)

            self.results.add_record(result, netflow.get_netflow()[i], label)

            i = i + 1
            self.totals = self.totals + 1
            self.logger.update_progress(i*1./size)
