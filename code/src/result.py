
class Failure:

    def __init__(self, result, correct):
        self.result = result
        self.correct = correct

    def string(self):
        return "Expected " + str(self.correct) + " Got: " + str(self.result) + "\n"

# The failure records class
class Failures:

    def __init__(self):
        self.fails = 0
        self.records = []

    def add_fail_record(self, result, correct):
        self.records.append(Failure(result, correct))
        self.fails = self.fails + 1

    def results(self, totals, minimize=True):
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


# Class to keep all the results
class ResultManager:

    def __init__(self, logger, good_labels):
        self.logger = logger
        self.fails = Failures()
        self.total = 0
        self.good_labels = good_labels
        self.good_labels.append('non-malicous')

        self.false_neg = 0
        self.false_pos = 0
        self.true_pos = 0
        self.true_neg = 0

    # Add a record to the result class
    # This can also be logged in this class
    #
    # label = predicted output
    # flow = the flow data
    # correct = correct label
    #
    def add_record(self, label, flow, correct):
        self.total += 1
        self.check_output(label, flow, correct)

    # Compare labels strict
    def compare_strict(self, label, flow, correct):
        test = correct == label
        if not test:
            self.logger.output_check(correct, flow, label)
            self.fails.add_fail_record(correct, label)

    # Check if the label belongs to the good labels class
    def compare_good(self, label, flow):
        if label in self.good_labels:
            pass

    # Use standard checking for the output using labels
    # True positive = good data
    # Check for:
    #       false negative
    #       false positive
    #       true negative
    #       true positive
    def check_output(self, label, flow, correct):
        if label > 0:
            if correct in self.good_labels:
                self.true_pos += 1
            else:
                self.false_pos += 1
        else:
            if correct in self.good_labels:
                self.false_neg += 1
            else:
                self.true_neg += 1

    # Use standard checking for the output using labels
    # True positive = malicious data
    # Check for:
    #       false negative
    #       false positive
    #       true negative
    #       true positive
    def check_output(self, label, flow, correct):
        if label > 0:
            if correct not in self.good_labels:
                self.true_pos += 1
            else:
                self.false_pos += 1
        else:
            if correct not in self.good_labels:
                self.false_neg += 1
            else:
                self.true_neg += 1

    def get_output(self):
        s = self.fails.results(self.total) + "\n"
        s += "False negative: " + str(self.false_neg) + "\n"
        s += "False positive: " + str(self.false_pos) + "\n"
        s += "True negative: " + str(self.true_neg) + "\n"
        s += "True positive: " + str(self.true_pos) + "\n"
        return s
