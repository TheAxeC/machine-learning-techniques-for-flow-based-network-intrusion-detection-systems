
# Base class for algorithms
class MLAlgorithm:

    def __init__(self):
        self.save = None
        self.save_file = None
        self.algorithm = None
        self.good_labels = []



    #def stop(self):
    #    if self.logger:
    #        self.logger.close()

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
        try:
            self.algorithm = joblib.load(file)
        except Exception as e:
            return False
        return True


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
            print e
            print "Algorithm \"" + str(name) + "\" does not exist."
            return None

#########################################################
### Baseline algorithms
#########################################################

class RandomClassifier(MLAlgorithm):

    def __init__(self):
        from sklearn import dummy
        self.algorithm = dummy.DummyClassifier(strategy='uniform')

    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]


class Plot_RandomClassifier(MLAlgorithm):

    def __init__(self):
        from sklearn import dummy
        self.algorithm = dummy.DummyClassifier(strategy='uniform')

    def train(self, data_set, target_set=None):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "Plot_RandomClassifier", data_set, target_set, cv=2, baseline=False)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class PureRandomClassifier(MLAlgorithm):

    def __init__(self):
        from sklearn import dummy
        self.algorithm = []

    def train(self, data_set, target_set=None):
        self.algorithm = list(set(target_set))

    # Predict a sample
    def predict(self, sample, corr=None):
        import random
        return random.choice(self.algorithm)

#########################################################
### Implemented algorithms UNSUPERVISED
#########################################################

# An unsupervised learning algorithm
class OneClassSVM(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.OneClassSVM(nu=0.01,
                                     kernel="rbf", gamma=0.1)

    # Train the data set
    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        output = self.algorithm.predict([sample])[0]

        if output > 0:
            return 'non_malicious'
        else:
            return 'malicious'

    def record_predict(self, flow, features, logger):
        output = self.algorithm.predict([features])[0]

# An unsupervised learning algorithm
class OneClassSVMGood(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.OneClassSVM(nu=0.01,
                                     kernel="rbf", gamma=0.1)

    # Train the data set
    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        output = self.algorithm.predict([sample])[0]

        if output < 0:
            return 'non_malicious'
        else:
            return 'malicious'

class MeanShift(MLAlgorithm):
    def __init__(self):
        from sklearn import cluster
        self.algorithm = cluster.MeanShift()

    # Train the data set
    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class KMeans(MLAlgorithm):
    def __init__(self):
        from sklearn import cluster
        self.algorithm = cluster.KMeans(n_clusters = 70)

    # Train the data set
    def train(self, data_set, target_set=None):
        return self.algorithm.fit_predict(data_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

#########################################################
### Implemented algorithms SUPERVISED
#########################################################

class DecisionTreeClassifier(MLAlgorithm):
    def __init__(self):
        from sklearn import tree
        self.algorithm = tree.DecisionTreeClassifier()

    # Train the data set
    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class GaussianNB(MLAlgorithm):
    def __init__(self):
        from sklearn import naive_bayes
        self.algorithm = naive_bayes.GaussianNB()

    # Train the data set
    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class NeuralNetwork(MLAlgorithm):
    def __init__(self):
        from sklearn import neural_network
        self.algorithm = neural_network.MLPClassifier(algorithm='l-bfgs', activation='logistic', hidden_layer_sizes=(15, 15, 15, 15, 15))

    # Train the data set
    def train(self, data_set, target_set=None):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the SVM machine learning algorithm
class SupportVectorMachine(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.SVC()

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class LinearSVC(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.LinearSVC()

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
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
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifierEucl(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='euclidean')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifierCheb(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='chebyshev')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifierCanberra(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='canberra')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifier3(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(n_neighbors=3, weights='distance', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifier7(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(n_neighbors=7, weights='distance', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class KNeighborsClassifierUniform(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='uniform', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

#########################################################
### Visualisation algorithms
#########################################################


class Plot_NeuralNetwork(MLAlgorithm):
    def __init__(self):
        from sklearn import neural_network
        self.algorithm = neural_network.MLPClassifier(hidden_layer_sizes=(500, 500, 500, 500, 500), max_iter=2000, )

    # Train the data set
    def train(self, data_set, target_set=None):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "NeuralNetwork", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class Plot_KNeighborsClassifier(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "KNeighborsClassifier Distance", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class Plot_KNeighborsClassifier_minkowski(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='chebyshev')

    # Train the data set
    def train(self, data_set, target_set):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "KNeighborsClassifier Distance with Minkowski", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class Plot_show_KNeighborsClassifier(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='distance', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "KNeighborsClassifier Distance", data_set, target_set, cv=2, save=False)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]


# Using the KNeighborsClassifier machine learning algorithm
class Plot_KNeighborsClassifierUniform(MLAlgorithm):
    def __init__(self):
        from sklearn import neighbors
        self.algorithm = neighbors.KNeighborsClassifier(weights='uniform', p=1, metric='manhattan')

    # Train the data set
    def train(self, data_set, target_set):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "KNeighborsClassifier Uniform", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

# Using the KNeighborsClassifier machine learning algorithm
class Plot_SupportVectorMachine(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.SVC()

    # Train the data set
    def train(self, data_set, target_set):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "Support Vector Machine", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class Plot_DecisionTreeClassifier(MLAlgorithm):
    def __init__(self):
        from sklearn import tree
        self.algorithm = tree.DecisionTreeClassifier()

    # Train the data set
    def train(self, data_set, target_set=None):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "DecisionTreeClassifier", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class Plot_GaussianNB(MLAlgorithm):
    def __init__(self):
        from sklearn import naive_bayes
        self.algorithm = naive_bayes.GaussianNB()

    # Train the data set
    def train(self, data_set, target_set=None):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "Gaussian Naive Bayes", data_set, target_set, cv=2)
        self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

class Plot_LinearSVC(MLAlgorithm):
    def __init__(self):
        from sklearn import svm
        self.algorithm = svm.LinearSVC()

    # Train the data set
    def train(self, data_set, target_set):
        from visualise import plot_learning_curve
        plot_learning_curve(self.algorithm, "Linear Support Vector Machine", data_set, target_set, cv=2)
        #self.algorithm.fit(data_set, target_set)

    # Predict a sample
    def predict(self, sample, corr=None):
        return self.algorithm.predict([sample])[0]

#########################################################
### Special Aggregation container
#########################################################

class AlgorithmContainer(MLAlgorithm):

    def __init__(self):
        self.supervised = KNeighborsClassifier() #KNeighborsClassifier()
        self.unsupervised = None#KMeans()

        # Also store the labels in this class
        self.clusters = []
        for i in xrange(0, 200):
            self.clusters.append({})

    def get_label(self, clus):
        m = ""
        ma = 0
        for key,val in self.clusters[clus].iteritems():
            if val > ma:
                ma = val
                m = key
        return m

    # Train the data set
    def train(self, data_set, target_set):
        if self.supervised:
            self.supervised.train(data_set, target_set)
        if self.unsupervised:
            totals = self.unsupervised.train(data_set, target_set)
            i = 0
            for ind in totals:
                res = target_set[i]
                if res in self.clusters[ind]:
                    self.clusters[ind][res] += 1
                else:
                    self.clusters[ind][res] = 1
                i += 1

    # Predict a sample
    def predict(self, sample, corr=None):
        supr = self.supervised.predict(sample)
        #ussupr = self.unsupervised.predict(sample)

        #print str(self.get_label(ussupr)) + " " + str(supr) + " " + str(corr)
        return supr
        return str(self.get_label(ussupr))
