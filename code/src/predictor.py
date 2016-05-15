
# A predictor class
class Predictor:

    # Initialisation of variables
    def __init__(self):
        self.start = 0
        self.finish = 0

        self.algorithm = None
        self.feature = None

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
    def runner(self, data_set):
        for d in data_set:
            try:
                samples = self.predict_raw(d)
                if samples:
                    print "Using " + str(samples.get_size()) + " samples."
                    print "Start predicting..."
                    self.predict(samples)
            except KeyboardInterrupt as e:
                self.logger.update_progress(-1)
                print "KeyboardInterrupt occured..."
            print "End prediction."
        try:
            print self.results.get_output()
        except Exception as e:
            pass

    # Check whether the key exists
    def check_keys(self, dic, key, val):
        if not key in dic:
            dic[key] = val
        return dic[key]

    # Predict the elements in a file
    def predict_raw(self, data):
        key = self.check_keys(data, "type", "PredictionFile")
        from prediction_type import PredictionFile, PredictionLoader
        loader = PredictionLoader.get_loader(key, PredictionFile())
        print "Loaded prediction loader: " + str(key) + "."
        return loader.load(data, self)

    # Predict a single flow file that has been loaded
    def predict(self, flow):
        if self.algorithm:
            self.loop(flow)
        else:
            print "Please set an algorithm first."

    def predict_sample(self, flow, label, flow_raw):
        result = self.algorithm.predict(flow, label)
        self.results.add_record(result, flow_raw, label)

    def loop(self, netflow):
        i = 0
        size = netflow.get_size()

        while i < size:
            flow_raw = netflow.get_netflow()[i]
            flow = netflow.get_sample_data(self.feature, i)
            label =  netflow.get_target_data()[i]
            self.predict_sample(flow, label, flow_raw)

            i = i + 1
            self.logger.update_progress(i*1./size)
