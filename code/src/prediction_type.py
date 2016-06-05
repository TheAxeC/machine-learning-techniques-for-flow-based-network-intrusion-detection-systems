class PredictionLoader:
    @staticmethod
    def get_loader(name, default=None):
        import sys

        try:
            return getattr(sys.modules[__name__], name)()
        except Exception as e:
            print "PredictionLoader \"" + name + "\"does not exist."
            return default

    # Check whether the key exists
    def check_keys(self, dic, key, val):
        if not key in dic:
            dic[key] = val
        return dic[key]

class PredictionFile(PredictionLoader):
    def load(self, data, predictor):
        self.check_keys(data, "from", 0)
        self.check_keys(data, "file", "")
        self.check_keys(data, "to", -1)
        print "Start file: " + str(data['file']) + "."

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(data['file'], data['from'], data['to'], None, False):
            print "Dataset \"" + data['file'] + "\" could not be loaded."
            return None

        return loader.get_netflow()

class PredictionFileBadSamples(PredictionLoader):
    def load(self, data, predictor):
        self.check_keys(data, "from", 0)
        self.check_keys(data, "file", "")
        self.check_keys(data, "to", -1)
        print "Start file: " + str(data['file']) + "."

        from loader import Loader, CTULoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "CTULoader"), CTULoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(data['file'], data['from'], data['to'], predictor.get_good_labels(), False):
            print "Dataset \"" + data['file'] + "\" could not be loaded."
            return None

        return loader.get_netflow()

class PredictionSQL(PredictionLoader):
    def load(self, data, predictor):
        host = self.check_keys(data, "host", "")
        user = self.check_keys(data, "user", "")
        password = self.check_keys(data, "password", "")
        db = self.check_keys(data, "db", "")
        amount = self.check_keys(data, "amount", 2000)
        print "Start file: " + host+":"+db + "."

        from loader import Loader, PickleLoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "PickleLoader"), PickleLoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(host, user, password, db, amount, classify=True, db_file=predictor.get_db_file()):
            print "Dataset \"" + host+":"+db + "\" could not be loaded."
            return None
        return loader.get_netflow()

class PredictionBinary(PredictionLoader):
    def load(self, data, predictor):
        f = self.check_keys(data, "file", "")
        amount = self.check_keys(data, "amount", -1)
        print "Start file: " + str(data['file']) + "."

        from loader import Loader, BinaryLoader
        loader = Loader.get_loader(self.check_keys(data, "loader", "BinaryLoader"), BinaryLoader())
        print "Using Loader \"" + data["loader"] + "\" to load the data."

        if not loader.load(f, amount, predictor):
            print "Dataset \"" + data['file'] + "\" could not be loaded."
            return None
        return None
