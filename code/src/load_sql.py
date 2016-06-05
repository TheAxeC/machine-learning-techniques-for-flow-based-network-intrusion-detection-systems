

def load_sql(host, user, password, db, amount):
    from loader import SQLLoader
    loader = SQLLoader()

    loader.load(host, user, password, db, amount, classify=True)
    netflow = loader.get_netflow()
    return netflow

import json
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        from flow import Flows
        if not isinstance(obj, Flows):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__

def save_netflow(file_name, netflow):
    import pickle
    pickle.dump( netflow, open( file_name, "w+" ) )

import sys
if __name__ == "__main__":
    file_name = "./test/db.json"
    netflow = load_sql("localhost", "root", "Kronos1994", "dataset", 300000)
    print netflow.__dict__
    print netflow.get_size()
    save_netflow(file_name, netflow)
