
class SingleResult:

    def __init__(self):
        self.m_fscore = 0
        self.m_prec = 0
        self.m_rec = 0

        self.b_fscore = 0
        self.b_prec = 0
        self.b_rec = 0

        self.samples = 0
        self.cor = 0
        self.false_neg = 0
        self.false_pos = 0
        self.true_neg = 0
        self.true_pos = 0

        self.pos_train = 0
        self.neg_train = 0

    def get_dict(self):
        return self.__dict__

    def print_result(self, name):
        s = ""
        s += '\\caption{' + name + '.}' + "\n"
        s += '\\label{}' + "\n"
        s += '\\centering' + "\n"
        s += '\\begin{tabular}{l r}' + "\n"
        s += '\\toprule' + "\n"
        s += 'Multi-class F-score & ' + str(self.m_fscore) + " \\\\" + "\n"
        s += 'Multi-class Precision & ' + str(self.m_prec)  + " \\\\" + "\n"
        s += 'Multi-class Recall & ' + str(self.m_rec) + " \\\\" + "\n"
        s += '\\midrule' + "\n"
        s += 'Binary F-score & ' + str(self.b_fscore) + " \\\\" + "\n"
        s += 'Binary Precision & ' + str(self.b_prec) + " \\\\" + "\n"
        s += 'Binary Recall & ' + str(self.b_rec) + " \\\\" + "\n"
        s += '\\midrule' + "\n"
        s += 'Total amount of samples & ' + str(self.samples) + " \\\\" + "\n"
        s += 'Correctly classified & ' + str(self.cor) + '%' + " \\\\" + "\n"
        s += 'False negative & ' + str(self.false_neg) + " \\\\" + "\n"
        s += 'False positive & ' + str(self.false_pos) + " \\\\" + "\n"
        s += 'True negative & ' + str(self.true_neg) + " \\\\" + "\n"
        s += 'True positive & ' + str(self.true_pos) + " \\\\" + "\n"
        s += '\\midrule' + "\n"
        s += 'Positive training samples & ' + str(self.pos_train) + " \\\\" + "\n"
        s += 'Negative training samples & ' + str(self.neg_train) + " \\\\" + "\n"
        s += '\\bottomrule' + "\n"
        s += '\\end{tabular}' + "\n"
        return s

class ResultManager:

    def __init__(self):
        self.results = []
        self.cur = None

    def add_new_result(self, pos_train, neg_train):
        self.cur = SingleResult()
        self.results.append(self.cur)

        self.cur.pos_train = pos_train
        self.cur.neg_train = neg_train

    def copy_new_result(self):
        cur = SingleResult()

        cur.pos_train = self.cur.pos_train
        cur.neg_train = self.cur.neg_train

        self.cur = cur
        self.results.append(self.cur)

    def add_result_multiclass(self, fscore, prec, recall):
        self.cur.m_fscore = fscore
        self.cur.m_prec = prec
        self.cur.m_rec = recall

    def add_result_binary(self, fscore, prec, recall):
        self.cur.b_fscore = fscore
        self.cur.b_prec = prec
        self.cur.b_rec = recall

    def add_result_samples(self, samples, cor, false_neg, false_pos, true_neg, true_pos):
        self.cur.samples = samples
        self.cur.cor = cor
        self.cur.false_neg = false_neg
        self.cur.false_pos = false_pos
        self.cur.true_neg = true_neg
        self.cur.true_pos = true_pos

    def get_average_result(self):
        result = SingleResult()
        for key in result.get_dict():
            val = 0.0
            for item in self.results:
                val += item.get_dict()[key]
            try:
                result.get_dict()[key] = val / len(self.results)
            except ZeroDivisionError:
                result.get_dict()[key] = -1
        return result

    def get_variance(self, avg):
        result = SingleResult()
        for key in result.get_dict():
            val = 0.0
            for item in self.results:
                val += (avg.get_dict()[key] - item.get_dict()[key]) ** 2
            try:
                result.get_dict()[key] = val / len(self.results)
            except ZeroDivisionError:
                result.get_dict()[key] = -1
        return result

    def print_results(self, name):
        avg = self.get_average_result()
        var = self.get_variance(avg)

        i = 1
        for item in self.results:
            print '++++++++++++++++++++'
            print item.print_result(name + ': Experiment ' + str(i))
            i += 1
        print '++++++++++++++++++++'
        print avg.print_result(name + ': Average')
        print '++++++++++++++++++++'
        print var.print_result(name + ': Variance')
        print '++++++++++++++++++++'

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
        if totals == 0:
            return "No predictions to check"

        ret = "Ratio of: " + str(float(totals - self.fails) / float(totals) * 100.0) + "% with " + str(self.fails) + " fails and"
        ret += " a total of " + str(totals) + " precictions"

        if minimize:
            return ret

        ret += "\n"
        for f in self.records:
            ret += f.string()
        ret += "\n"

        return ret

    def percentage(self, totals):
        return float(totals - self.fails) / float(totals) * 100.0

class FirewallLogs:

    def __init__(self):
        self.keys = []
        self.data = {}

    def open_files(self, files):
        import os
        for f in files:
            if os.path.isdir(f):
                mypath = f
                onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
                for f in onlyfiles:
                    self.open_single_file(f)
            elif os.path.isfile(f):
                self.open_single_file(f)

    def open_single_file(self, file_name):
        import csv
        with open(file_name, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            rownum = 0
            for row in reader:
                if rownum == 0:
                    self.keys = row
                else:
                    self.data[row[3]] = row

                rownum += 1
                if rownum > 100000:
                    break

    def contains(self, ip):
        return ip in self.data


# Class to keep all the results
class ResultPrediction:

    def __init__(self, logger, good_labels, manager):
        self.logger = logger
        self.fails = Failures()
        self.total = 0
        self.good_labels = good_labels
        self.good_labels.append('non-malicous')

        self.false_neg = 0
        self.false_pos = 0
        self.true_pos = 0
        self.true_neg = 0

        self.ground_truth = []
        self.predictions = []

        self.ground_truth_bin = []
        self.predictions_bin = []

        self.predictions_unknown = []

        self.manager = manager

    # Add a record to the result class
    # This can also be logged in this class
    #
    # label = predicted output
    # flow = the flow data
    # correct = correct label
    #
    def add_record(self, label, flow, correct):
        self.total += 1
        self.add_evaluation(label, correct)
        self.compare_strict(label, flow, correct)

        self.store_result(label, correct)

    def add_record_unknown(self, label, flow):
        flow.prediction = label
        self.predictions_unknown.append(flow)

    def store_result(self, label, correct):
        self.ground_truth.append(correct)
        self.predictions.append(label)

        self.ground_truth_bin.append(int(correct not in self.good_labels))
        self.predictions_bin.append(int(label not in self.good_labels))

    # Compare labels strict
    def compare_strict(self, label, flow, correct):
        test = correct == label
        if not test:
            self.logger.output_check(correct, flow, label)
            self.fails.add_fail_record(label, correct)

    def calculate_scoring(self):
        from sklearn import metrics

        s = ""
        try:
                #items = self.ground_truth + self.predictions
                #set = {}
                #map(set.__setitem__, items, [])
                #labels = set.keys()
                #s += "Labels used: " + str(labels) + "\n"

            try:
                f1 = metrics.f1_score(self.ground_truth, self.predictions, average='weighted')
                s += "F1 score: " + str(f1) + "\n"
                prec = metrics.precision_score(self.ground_truth, self.predictions, average='weighted')
                s += "Precision score: " + str(prec) + "\n"
                rec = metrics.recall_score(self.ground_truth, self.predictions, average='weighted')
                s += "Recall score: " + str(rec) + "\n"
                acc = metrics.accuracy_score(self.ground_truth, self.predictions)
                s += "Accuracy score: " + str(acc) + "\n"
                self.manager.add_result_multiclass(f1, prec, rec)
            except Exception as e:
                pass

            s += "\n"

            f1 = metrics.f1_score(self.ground_truth_bin, self.predictions_bin)
            s += "F1 score Binary: " + str(f1) + "\n"
            prec = metrics.precision_score(self.ground_truth_bin, self.predictions_bin)
            s += "Precision score Binary: " + str(prec) + "\n"
            rec = metrics.recall_score(self.ground_truth_bin, self.predictions_bin)
            s += "Recall score Binary: " + str(rec) + "\n"
            acc = metrics.accuracy_score(self.ground_truth_bin, self.predictions_bin)
            s += "Accuracy score Binary: " + str(acc) + "\n"
            self.manager.add_result_binary(f1, prec, rec)

            s += "classification report: \n"
            s += metrics.classification_report(self.ground_truth, self.predictions)
            s += "\n"
            s += "Predictions:\n"
            from collections import Counter
            col = Counter(self.predictions)
            for key, value in col.iteritems():
                s += str(key) + " => " + str(value) + "\n"
        except Exception as e:
            import traceback
            traceback.print_exc()

        return s

    def get_output(self, config):
        s = ""
        if self.total > 0:
            s += self.fails.results(self.total, True) + "\n"
            s += "False negative: " + str(self.false_neg) + "\n"
            s += "False positive: " + str(self.false_pos) + "\n"
            s += "True negative: " + str(self.true_neg) + "\n"
            s += "True positive: " + str(self.true_pos) + "\n"
            s += "\n"
            self.manager.add_result_samples(self.total, self.fails.percentage(self.total),
                    self.false_neg, self.false_pos, self.true_neg, self.true_pos)

            try:
                prec = float(self.true_pos) / float(self.true_pos + self.false_pos)
            except ZeroDivisionError:
                prec = float('Inf')

            try:
                rec = float(self.true_pos) / float(self.true_pos + self.false_neg)
            except ZeroDivisionError:
                rec = float('Inf')

            try:
                f1 = (2 * prec * rec) / (prec + rec)
            except ZeroDivisionError:
                f1 = float('Inf')

            s += "Precision: " + str(prec) + "\n"
            s += "Recall: " + str(rec) + "\n"
            s += "Fscore: " + str(f1) + "\n"

            s += "\n"
            s += self.calculate_scoring()
        s += self.get_prediction_results(config)
        return s

    def get_prediction_results(self, config):
        csv = None
        if len(self.predictions_unknown) > 0:
            csv = FirewallLogs()
            csv.open_files(config.get_firewall_logs())
            print "Opened firewall logs"
        else:
            return

        self.manager.copy_new_result()

        false_neg = 0
        false_pos = 0
        true_pos = 0
        true_neg = 0
        total = len(self.predictions_unknown)
        for flow in self.predictions_unknown:
            pos = flow.prediction not in self.good_labels

            if csv.contains(flow.dest_ip) or csv.contains(flow.src_ip):
                if pos:
                    true_pos += 1
                else:
                    false_neg += 1
            else:
                if pos:
                    false_pos += 1
                else:
                    true_neg += 1

            #s += flow.prediction
            #if flow.prediction not in self.good_labels:
            #    s += "Flow is malicious:"
            #    s += "\tStarting time: " + str(flow.start_time)
            #    s += "\tDuration: " + str(flow.duration)
            #    s += "\tProtocol: " + str(flow.protocol)
            #    s += "\tTotal bytes: " + str(flow.total_bytes)
            #    s += "\tTotal packets: " + str(flow.total_pckts)
            #    s += "\tSource and destination IP: " + str(flow.src_ip) + " || " + str(flow.dest_ip)
            #    s += "\tSourse and destination Port: " + str(flow.src_port) + " || " + str(flow.dest_port)
            #    s += ""

        self.manager.add_result_samples(total, 0,
                false_neg, false_pos, true_neg, true_pos)
        try:
            prec = float(true_pos) / float(true_pos + false_pos)
        except ZeroDivisionError:
            prec = float('Inf')

        try:
            rec = float(true_pos) / float(true_pos + false_neg)
        except ZeroDivisionError:
            rec = float('Inf')

        try:
            f1 = (2 * prec * rec) / (prec + rec)
        except ZeroDivisionError:
            f1 = float('Inf')

        self.manager.add_result_binary(f1, prec, rec)

        return ""

    def add_evaluation(self, label, correct):
        if label in self.good_labels:
            if correct in self.good_labels:
                self.true_neg += 1
            else:
                self.false_neg += 1
        else:
            if correct in self.good_labels:
                self.false_pos += 1
            else:
                self.true_pos += 1
