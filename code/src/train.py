
# The trainer class
# Can be used to do the main training
# Base class
class Trainer(object):

    def __init__(self):
        from flow import Flows
        self.flow = Flows()

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels, config):
        key = self.check_keys(data, "type", "DefaultTrainer")
        trainer = Trainer.get_trainer(key, DefaultTrainer())
        print "Loaded training algorithm: " + str(key) + "."
        fl = trainer.train(algorithm, data, feature, good_labels, config)
        if not fl:
            return False
        else:
            self.flow.addFlows(fl)
            return True

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

    def trainAll(self, feature, algorithm, good_labels, manager):
        samples = self.flow.get_sample_data_complete(feature)
        targets = self.flow.get_target_data()
        if len(samples) > 2:
            algorithm.train(samples, targets)
            pos_train = 0
            neg_train = 0
            for i in targets:
                if i in good_labels:
                    neg_train += 1
                else:
                    pos_train += 1
            manager.add_new_result(pos_train, neg_train)

    def default(self, algorithm, loader, feature, file):
        print "Training size is " + str(loader.get_netflow().get_size()) + "."

        if loader.get_netflow().get_size() <= 2:
            print "Training set too small."
            return None
        #else:
        #    samples = loader.get_netflow().get_sample_data_complete(feature)
        #    targets = loader.get_netflow().get_target_data()
        #    #try:
        #    algorithm.train(samples, targets)
        #    #except Exception as e:
        #    #    raise e
        #    #    print "Wrong training data set used."
        #    #    return False

        print "Training set \"" + file + "\"  done."
        return loader.get_netflow()

class PlotTrainer(Trainer):

    def trainAll(self, feature, algorithm, good_labels, manager):
        self.flow = self.flow.random()
        super(PlotTrainer, self).trainAll(feature, algorithm, good_labels, manager)

# default netflow trainer
class DefaultTrainer(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels, config):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to):
            print "Training set \"" + file + "\" could not be loaded."
            return None

        return self.default(algorithm, loader, feature, file)

# Trains an algorithm with only good (non-malicious) data
class GoodTrainer(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels, config):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to, good_labels):
            print "Training set \"" + file + "\" could not be loaded."
            return None

        return self.default(algorithm, loader, feature, file)

# Trains an algorithm with only bad (malicious) data
class BadTrainer(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels, config):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)
        amount = self.check_keys(data, "amount", -1)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to, good_labels, False, amount=amount):
            print "Training set \"" + file + "\" could not be loaded."
            return None

        return self.default(algorithm, loader, feature, file)

# Trains an algorithm with only bad (malicious) data
class BadTrainerPlus(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, data, feature, good_labels, config):
        fr = self.check_keys(data, "from", 0)
        file = self.check_keys(data, "file", "")
        to = self.check_keys(data, "to", -1)
        amount = self.check_keys(data, "amount", -1)
        amountOther = self.check_keys(data, "amountOther", 0)

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(file, fr, to, good_labels, False, amount=amount, amountGood=amountOther):
            print "Training set \"" + file + "\" could not be loaded."
            return None

        return self.default(algorithm, loader, feature, file)

# Class to train with data from an SQL database
class SQLTrainer(Trainer):

    def train(self, algorithm, data, feature, good_labels, config):
        host = self.check_keys(data, "host", "")
        user = self.check_keys(data, "user", "")
        password = self.check_keys(data, "password", "")
        db = self.check_keys(data, "db", "")
        amount = self.check_keys(data, "amount", 10000)

        from loader import Loader, PickleLoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "PickleLoader"), PickleLoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(host, user, password, db, amount, classify=True, db_file=config.get_db_file()):
            print "Training set \"" + host+":"+db + "\" could not be loaded."
            return None

        return self.default(algorithm, loader, feature, host+":"+db)
