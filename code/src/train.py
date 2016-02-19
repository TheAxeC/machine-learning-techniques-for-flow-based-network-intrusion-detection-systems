

# The trainer class
# Can be used to do the main training
class Trainer:

    def __init__(self):
        pass

    # Train supervised with samples and targets
    def train(self, algorithm, file):
        pass

    @staticmethod
    def get_trainer(name):
        import sys

        try:
            return getattr(sys.modules[__name__], name)()
        except Exception as e:
            print "Trainer does not exist."
            return None

# Supervised netflow trainer
class NetflowTrainerS(Trainer):

    # Train supervised with samples and targets
    def train(self, algorithm, file, fr, to):
        from loader import NetflowLoader
        loader = NetflowLoader()
        loader.load(file, fr, to)

        print "Training size is " + str(loader.get_netflow().get_size()) + "."

        samples = loader.get_netflow().get_sample_data()
        targets = loader.get_netflow().get_target_data()
        algorithm.train(samples, targets)

        print "Training set " + file + " done."
