

# The config class
class Config:

    def __init__(self, file_name=None):
        if not file_name:
            file_name = 'config.json'
        self.default = file_name
        self.path = ""
        self.data = {}

        self.configs = []

    def read_config_str(self, str_config, directory, data):
        import json
        import os
        import copy

        try:
            self.data = copy.deepcopy(data)
            if 'name' in self.data:
                del self.data['name']
            self.data.update( str_config )
            self.path = directory

            self.add_directory("pcap-files", ["src", "dest"])
            self.add_directory("data-sets", ["file"])
            self.add_directory("check-sets", ["file"])

            return True
        except Exception as e:
            import traceback
            traceback.print_exc()
            print e
            return False

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

            self.make_configs()

            self.add_directory("pcap-files", ["src", "dest"])
            self.add_directory("data-sets", ["file"])
            self.add_directory("check-sets", ["file"])

            return True
        except Exception as e:
            print e
            return False

    def make_configs(self):
        if 'use_main' in self.data and self.data['use_main']:
            self.data['name'] = 'Main'
            self.configs.append(self)
        if 'configs' in self.data:
            config_list = self.data['configs']

            if not type(config_list) is list:
                return
            for d in config_list:
                c = Config()
                if c.read_config_str(d, self.path, self.data):
                    self.configs.append(c)

    def get_name(self):
        if 'name' in self.data:
            return self.data['name']
        return "defaultName"

    def get_description(self):
        if 'description' in self.data:
            return self.data['description']
        return "No description given"

    def get_configs(self):
        return self.configs

    def add_directory(self, name, features):
        if not name in self.data:
            return

        arr = self.data[name]
        for rec in arr:
            for f in features:
                try:
                    rec[f] = self.path + rec[f]
                except:
                    pass

    def get_config_log(self):
        return self.path + "logs/log_" + self.get_name() + ".txt"

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
            return feature.BasicFeature.get_feature(self.data['featureClass'], self)
        elif "featureClass" in self.data:
            return feature.BasicFeature.get_feature(self.data['featureClass'], self)
        return None

    def get_feature_file(self):
        if "feature-file" in self.data:
            return self.path + self.data['feature-file']
        return self.path + 'features.json'

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

    def get_amount(self):
        if 'amount' in self.data:
            return self.data['amount']
        return 1

    # Get trainer class
    def get_trainer(self):
        from train import Trainer
        if 'trainer' in self.data:
            return Trainer.get_trainer(self.data['trainer'])
        return Trainer.get_trainer('Trainer')

    def get_trainer_name(self):
        if 'trainer' in self.data:
            return self.data['trainer']
        return "Trainer"

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

    # Get the flow timeout
    def get_flow_timeout(self):
        if 'timeout' in self.data:
            return self.data['timeout']
        return 5000

    def get_protocol_file(self):
        if 'protocol-file' in self.data:
            return self.path + self.data['protocol-file']
        return self.path + "protocols.json"

    def get_logger_file(self):
        if 'logger' in self.data:
            return self.path + self.data['logger']
        return self.path + "log.txt"

    def get_good_labels_file(self):
        if 'good-labels' in self.data:
            return self.path + self.data['good-labels']
        return self.path + "good.txt"

    def print_labels(self):
        if 'print-labels' in self.data:
            return self.data['print-labels']
        return False

    def get_firewall_logs(self):
        if 'firewall_logs' in self.data:
            return self.data['firewall_logs']
        return ['./cegeka/2016-04-03_085630_83.log.textlog']

    def get_country_file(self):
        if 'country_file' in self.data:
            return self.path + self.data['country_file']
        return self.path + 'country_complete.json'

    def get_db_file(self):
        if 'db_file' in self.data:
            return self.path + self.data['db_file']
        return self.path + 'db.json'
