
# The trainer class
# Can be used to do the main training
# Base class
class Trainer:

    def __init__(self):
        pass

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels):
        key = self.check_keys(data, "type", "DefaultTrainer")
        trainer = Trainer.get_trainer(key, DefaultTrainer())
        print "Loaded training algorithm: " + str(key) + "."
        return trainer.train(algorithm, data, feature, good_labels)

    def check_keys(self, dic, key, val):
        if not key in dic:
            dic[key] = val
        return dic[key]

    @staticmethod
    def get_trainer(name, default=None):
        import sys

        try:
            return getattr(sys.modules[__name__], name)()
        except Exception as e:
            print "Trainer \"" + name + "\"does not exist."
            return default

    def default(self, algorithm, loader, feature, file):
        print "Training size is " + str(loader.get_netflow().get_size()) + "."

        if loader.get_netflow().get_size() <= 2:
            print "Training set too small."
            return False
        else:
            samples = loader.get_netflow().get_sample_data_complete(feature)
            targets = loader.get_netflow().get_target_data()
            try:
                algorithm.train(samples, targets)
            except Exception as e:
                raise e
                print "Wrong training data set used."
                return False

        print "Training set \"" + file + "\"  done."
        return True

# default netflow trainer
class DefaultTrainer(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to):
            print "Training set \"" + file + "\" could not be loaded."
            return False

        return self.default(algorithm, loader, feature, file)

# Trains an algorithm with only good (non-malicious) data
class GoodTrainer(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to, good_labels):
            print "Training set \"" + file + "\" could not be loaded."
            return False

        return self.default(algorithm, loader, feature, file)

# Trains an algorithm with only bad (malicious) data
class BadTrainer(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to, good_labels, False):
            print "Training set \"" + file + "\" could not be loaded."
            return False

        return self.default(algorithm, loader, feature, file)

# Class to train with data from an SQL database
class SQLTrainer(Trainer):

    def train(self, algorithm, data, feature, good_labels):
        host = self.check_keys(data, "host", "")
        user = self.check_keys(data, "user", "")
        password = self.check_keys(data, "password", "")
        db = self.check_keys(data, "db", "")
        amount = self.check_keys(data, "amount", 10000)

        from loader import Loader, SQLLoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "SQLLoader"), SQLLoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(host, user, password, db, amount):
            print "Training set \"" + host+":"+db + "\" could not be loaded."
            return False

        return self.default(algorithm, loader, feature, host+":"+db)
