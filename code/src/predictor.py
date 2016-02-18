
# The failure records class
class Failures:

    def __init__(self):
        self.fails = 0
        self.records = []

    def add_fail_record(self, result, correct):
        self.records.append("Expected " + netflow.get_target_data()[i] + " Got: " + result + "\n")
        self.fails = self.fails + 1

    def results(self, totals, minimize=False):
        ret = "Ratio of: " + str(self.fails / totals) + " with " self.fails + " fails and"
        ret += " a total of " + totals + " precictions\n"

        if minimize:
            return f

        for f in self.records:
            ret += f

        return f

# A predictor class
class Predictor:

    def __init__(self):
        self.totals = 0
        self.fails = Failures()

        self.start = 0
        self.finish = 0
        self.check = False

        self.algorithm = None

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def predict(self, flow, start=None, finish=None, check=False):
        if self.algorithm:
            self.settings(start, finish, check)
            self.loop(flow)
        else:
            print "Please set an algorithm first."

    def settings(self, start, finish, check):
        if not start:
            start = 0
        if not finish:
            finish = flow.get_size()
        self.start = start
        self.finish = finish
        self.check = check

    def loop(self, netflow):
        i = self.start
        while  < self.finish:
            result = algorithm.predict(netflow.get_sample_data()[i])
            if self.check:
                test = result == netflow.get_target_data()[i]
                if not test:
                    self.fails.add_fail_record(result, netflow.get_target_data()[i])
            i = i + 1
            self.totals = self.totals + 1

    def results(self):
        if check:
            return self.fails.results(self.totals, minimize=True)
        return None
