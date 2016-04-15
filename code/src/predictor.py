
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
    def runner(self, data_set):
        for d in data_set:
            try:
                samples = self.predict_raw(d)
                print "Using " + str(samples.get_size()) + " samples."
                if samples:
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
    def predict_raw(self, d):
        key = self.check_keys(d, "type", "file")
        good = self.check_keys(d, "good", False)
        try:
            meth = getattr(self, 'predict_'+key)
            return meth(d, good)
        except Exception as e:
            print e
            return None

    def predict_sql(self, data, good):
        host = self.check_keys(data, "host", "")
        user = self.check_keys(data, "user", "")
        password = self.check_keys(data, "password", "")
        db = self.check_keys(data, "db", "")
        amount = self.check_keys(data, "amount", 2000)
        print "Start file: " + host+":"+db + "."

        from loader import Loader, SQLLoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "SQLLoader"), SQLLoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(host, user, password, db, amount, good):
            print "Dataset \"" + host+":"+db + "\" could not be loaded."
            return None
        return loader.get_netflow()

    def predict_file(self, d, good):
        self.check_keys(d, "from", 0)
        self.check_keys(d, "file", "")
        self.check_keys(d, "to", -1)
        print "Start file: " + str(d['file']) + "."

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(d, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + d["loader"] + "\" to load the data."

        if not loader.load(d['file'], d['from'], d['to'], None, False):
            print "Dataset \"" + d['file'] + "\" could not be loaded."
            return None

        return loader.get_netflow()

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
            flow = netflow.get_sample_data(self.feature, i)
            label =  netflow.get_target_data()[i]
            result = self.algorithm.predict(flow, label)
            self.results.add_record(result, netflow.get_netflow()[i], label)

            i = i + 1
            self.totals = self.totals + 1
            self.logger.update_progress(i*1./size)
