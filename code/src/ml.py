
# Base class for algorithms
class MLAlgorithm:

    def __init__(self):
        self.save = None
        self.save_file = None
        self.algorithm = None
        self.good_labels = []
        self.malicious_labels = []

    # Set the logging files:
    def start(self, log, good_label, malicious_labels):
        self.logger = self.open_file(log)
        self.good_labels = self.load_labels(good_label)
        self.malicious_labels = self.load_labels(malicious_labels)

    # load labels:
    def load_labels(self, file_name):
        labels = []
        try:
            with open(file_name) as f:
                for line in f:
                    labels.append(line.strip())
        except Exception as e:
            print "Could not open label file: \"" + file_name + "\"."
            return []
        return labels

    # Open a file
    def open_file(self, f):
        try:
            return open(f, "w")
        except IOError as e:
            print "Could not open file: \"" + f + "\"."
            return None

    def stop(self):
        if self.logger:
            self.logger.close()

    # Train the data set
    def train(self, data_set, target_set):
        pass

    # Predict a sample
    def predict(self, sample):
        pass

    # Save a model
    def save(self, file=None):
        if file:
            from sklearn.externals import joblib
            joblib.dump(self.algorithm, file)
            self.save_file = file
            return self.save_file
        else:
            import pickle
            self.save = pickle.dumps(self.algorithm)
            return self.save

    # Load model from filename
    def load_file(self, file):
        from sklearn.externals import joblib
        self.algorithm = joblib.load(file)

    # Load a model (either from memory or from file)
    def load(self, file=None, model=None, override=False):
        if self.save:
            if override and model:
                self.save = model
            if self.save:
                import pickle
                pickle.loads(self.save)
        else:
            if override and file and s:
                self.save_file = file
            if self.save_file:
                from sklearn.externals import joblib
                joblib.load(self.save_file)

    # Get the saved model
    def get_saved_model(self):
        return self.save

    # Get the filename of the saved model
    def get_saved_file(self):
        return self.save_file

    @staticmethod
    def get_algorithm(name):
        import sys

        try:
            return getattr(sys.modules[__name__], name)()
        except Exception as e:
            print "Algorithm \"" + str(name) + "\" does not exist."
            return None

# Using the SVM machine learning algorithm
class SupportVectorMachine(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.SVC()

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifier(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample):
        return self.algorithm.predict([sample])[0]

    # Estimate whether a sample is malicious or not
    def record_predict(self, flow, sample):
        label = self.predict(sample)

        if label in self.good_labels:
            self.logger.write("Good label found \"" + label + "\"\n")
        else:
            from geoipc import GeoIP
            gi = GeoIP('GeoIP.dat')

            self.logger.write("Malicious label found \"" + str(label) + "\"!!!!!!!!!!!\n")
            self.logger.write("\t protocol: " + str(flow.protocol) + "\n")
            self.logger.write("\t address: from: " + str(flow.src_ip) + " to " + str(flow.dest_ip) + "\n")
            self.logger.write("\t country origin: " + gi.country(flow.src_ip) + "\n")
            self.logger.write("\t country destination: " + gi.country(flow.dest_ip) + "\n")
            self.logger.write("\t ports: from: " + str(flow.src_port) + " to " + str(flow.dest_port) + "\n")
            self.logger.write("\t packets: " + str(flow.total_pckts) + " with " + str(flow.total_bytes) + " bytes\n")
            self.logger.write("\t duration: " + str(flow.duration) + " starting from " + str(flow.start_time) + "\n")
        self.logger.flush()
