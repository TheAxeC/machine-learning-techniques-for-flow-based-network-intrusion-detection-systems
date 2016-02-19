
# Base class for algorithms
class MLAlgorithm:

    def __init__(self):
        self.save = None
        self.save_file = None
        self.algorithm = None

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
            print "Algorithm does not exist."
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
