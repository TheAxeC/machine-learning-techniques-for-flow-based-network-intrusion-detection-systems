

# The config class
class Config:

    def __init__(self):
        self.default = 'config.json'
        self.data = {}

    # Reading the config file
    def read_config(self, file=None):
        import json

        try:
            file_name = None
            if file:
                file_name = file
            else:
                file_name = self.default

            with open(file_name) as data_file:
                self.data = json.load(data_file)
            return True
        except Exception as e:
            print e
            return False

    # Get the algorithm file
    def get_algorithm(self):
        from ml import MLAlgorithm
        if 'algorithm' in self.data:
            return MLAlgorithm.get_algorithm(self.data['algorithm'])
        return None

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

    # Get the check sets
    def get_check_sets(self):
        if 'check-sets' in self.data:
            return self.data['check-sets']
        return []

    # Get the predict data sets
    def get_predict_sets(self):
        if 'predict-sets' in self.data:
            return self.data['predict-sets']
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
            return self.data['model_dir']
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
            return self.data['pcap-files']
        return []

    # Is prevention active
    def prevention_active(self):
        if 'prevention' in self.data:
            return self.data['prevention']
        return False
