

# The config class
class Config:

    def __init__(self, file_name=None):
        if not file_name:
            file_name = 'config.json'
        self.default = file_name
        self.path = ""
        self.data = {}

    # Reading the config file
    def read_config(self, file=None):
        import json
        import os

        try:
            file_name = None
            if file:
                file_name = file
            else:
                file_name = self.default

            with open(file_name) as data_file:
                self.data = json.load(data_file)
            self.path = os.path.dirname(file_name) + "/"

            self.add_directory("pcap-files", ["src", "dest"])
            self.add_directory("data-sets", ["file"])
            self.add_directory("check-sets", ["file"])

            return True
        except Exception as e:
            print e
            return False

    def add_directory(self, name, features):
        arr = self.data[name]
        for rec in arr:
            for f in features:
                try:
                    rec[f] = self.path + rec[f]
                except:
                    pass


    # Get the algorithm file
    def get_algorithm(self):
        from ml import MLAlgorithm
        if 'algorithm' in self.data:
            return MLAlgorithm.get_algorithm(self.data['algorithm'])
        return None

    # Get the algorithm file
    def get_feature(self):
        import feature
        if "featureClass" in self.data and "feature-file" in self.data:
            return feature.BasicFeature.get_feature(self.data['featureClass'], self.path + self.data['feature-file'])
        return None

    def get_feature_name(self):
        if 'featureClass' in self.data:
            return self.data['featureClass']
        return "Unknown"

    def get_algorithm_name(self):
        if 'algorithm' in self.data:
            return self.data['algorithm']
        return "Unknown"

    # Get the data sets
    def get_data_sets(self):
        if 'data-sets' in self.data:
            return self.data['data-sets']
        return []

    # Get trainer class
    def get_trainer(self):
        from train import Trainer
        if 'trainer' in self.data:
            return Trainer.get_trainer(self.data['trainer'])
        return None

    def get_trainer_name(self):
        if 'trainer' in self.data:
            return self.data['trainer']
        return "Unknown"

    # Get the check sets
    def get_check_sets(self):
        if 'check-sets' in self.data:
            return self.data['check-sets']
        return []

    # Do we need to do the predictions
    def is_predict(self):
        if 'predict' in self.data:
            return self.data['predict']
        return False

    # Do we need to do checks
    def is_check(self):
        if 'check' in self.data:
            return self.data['check']
        return False

    # Should failed predictions be printed
    def print_fails(self):
        if 'print-fails' in self.data:
            return self.data['print-fails']
        return False

    # Check if we want to use a stored model
    def use_model(self):
        if 'use_model' in self.data:
            return self.data['use_model']
        return False

    # Get the model directory
    def get_model_dir(self):
        if 'model_dir' in self.data:
            return self.path + self.data['model_dir']
        return ""

    # Get the stored model
    def get_model(self):
        if 'model' in self.data:
            return self.data['model']
        return ""

    # Get the stored model
    def store_model(self):
        if 'store_model' in self.data:
            return self.data['store_model']
        return False

    # Check if the IDS is enabled
    def enabled(self):
        if 'enable-IDS' in self.data:
            return self.data['enable-IDS']
        return True

    # Check if the sniffer is active
    def sniffer_active(self):
        if 'sniffer' in self.data:
            return self.data['sniffer']
        return False

    # Check if the packet analyser is active
    def packet_analyser_active(self):
        if 'packet-analyses' in self.data:
            return self.data['packet-analyses']
        return False

    # Check if the flow converter is active
    def flow_converter(self):
        if 'pcap-to-flow' in self.data:
            return self.data['pcap-to-flow']
        return False

    # Get the to-be-converted pcap files
    def pcap_files(self):
        if 'pcap-files' in self.data:
            for x in self.data['pcap-files']:
                if not 'src' in x:
                    x['src'] = ""
                if not 'dest' in x:
                    x['dest'] = None
            return self.data['pcap-files']
        return []

    # Is prevention active
    def prevention_active(self):
        if 'prevention' in self.data:
            return self.data['prevention']
        return False

    # Get the flow timeout
    def get_flow_timeout(self):
        if 'timeout' in self.data:
            return self.data['timeout']
        return 10

    def get_protocol_file(self):
        if 'protocol-file' in self.data:
            return self.path + self.data['protocol-file']
        return ""

    def get_logger_file(self):
        if 'logger' in self.data:
            return self.path + self.data['logger']
        return ""

    def get_good_labels_file(self):
        if 'good-labels' in self.data:
            return self.path + self.data['good-labels']
        return ""

    def print_labels(self):
        if 'print-labels' in self.data:
            return self.data['print-labels']
        return False
