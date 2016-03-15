class Failure:

    def __init__(self, result, correct, index):
        self.result = result
        self.correct = correct
        self.index = index

    def string(self):
        return "Expected " + str(self.correct) + " Got: " + str(self.result) + " Indexed " + str(self.index) + "\n"

# The failure records class
class Failures:

    def __init__(self):
        self.fails = 0
        self.records = []

    def add_fail_record(self, result, correct, i):
        self.records.append(Failure(result, correct, i))
        self.fails = self.fails + 1

    def results(self, totals, minimize=False):
        ret = "Ratio of: " + str(float(totals - self.fails) / float(totals) * 100.0) + "% with " + str(self.fails) + " fails and"
        ret += " a total of " + str(totals) + " precictions"

        if minimize:
            return ret

        ret += "\n"
        for f in self.records:
            ret += f.string()
        ret += "\n"

        return ret

class Result:

    def __init__(self, flow, result):
        self.flow = flow
        self.result = result



# A predictor class
class Predictor:

    def __init__(self, print_total=False):
        self.totals = 0
        self.fails = Failures()
        self.returns = []

        self.start = 0
        self.finish = 0
        self.check = False

        self.algorithm = None
        self.feature = None
        self.minimize = not print_total

    def set_feature(self, feature):
        self.feature = feature

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm
        self.logger = algorithm.logger

    def runner(self, data_set, check):
        for d in data_set:
            self.check_keys(d, "from", 0)
            self.check_keys(d, "file", "")
            self.check_keys(d, "to", -1)
            print "Start file: " + str(d['file']) + "."
            try:
                self.predict_file(d, check)
            except KeyboardInterrupt as e:
                self.logger.update_progress(-1)
                print "KeyboardInterrupt occured..."
            print "End file: " + str(d['file']) + "."
        print self.results()

    def check_keys(self, dic, key, val):
        if not key in dic:
            dic[key] = val

    def predict_file(self, d, check=False):
        from loader import NetflowLoader
        loader = NetflowLoader()
        if not loader.load(d['file'], d['from'], d['to']):
            print "Dataset \"" + d['file'] + "\" could not be loaded."
            return False

        samples = loader.get_netflow()
        print "Start predicting..."
        self.predict(samples, check=True)

    def predict(self, flow, check=False):
        if self.algorithm:
            self.check = check
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
            if self.check:
                #self.logger.output_complete(result, netflow.get_netflow()[i], self.algorithm.good_labels)
                test = result == label
                if not test:
                    self.logger.output_check(result, netflow.get_netflow()[i], label)
                    self.fails.add_fail_record(result, label, i)
            else:
                self.returns.append(Result(flow, result))
            i = i + 1
            self.totals = self.totals + 1
            self.logger.update_progress(i*1./size)

    def results(self):
        if self.check:
            return self.fails.results(self.totals, minimize=self.minimize)
        return self.returns

    def reset(self):
        self.totals = 0
        self.fails = Failures()
        self.returns = []

        self.start = 0
        self.finish = 0
        self.check = False
