
class Dummy:

    def get_good_labels(self):
        labels = []
        try:
            file_name = 'configs/main/good.txt'
            with open(file_name) as f:
                for line in f:
                    labels.append(line.strip())
        except Exception as e:
            print "Could not open label file: \"" + file_name + "\"."
            return []
        return labels

def do_request(add):
    #return '1;US;USA;United States'
    import urllib2
    return urllib2.urlopen("http://ip2c.org/" + add).read()


import json
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        from flow import Flows
        if not isinstance(obj, Flows):
            return super(MyEncoder, self).default(obj)

        return obj.__dict__

def save_dictionary(file_name, netflow):
    import pickle
    pickle.dump( netflow, open( file_name, "w+" ) )

def load_pickle(file_name):
    import pickle
    return pickle.load( open( file_name, "r+" ) )


def get_country(netflow, dic):
    print 'Running'
    i = 0
    for sample in netflow.get_netflow():
        src_ip = sample.src_ip
        dst_ip = sample.dest_ip
        print i

        if src_ip not in dic and is_IPv4(src_ip):
            # do request
            result = do_request(src_ip)
            print result
            dic[src_ip] = result

        if dst_ip not in dic and is_IPv4(dst_ip):
            # do request
            result = do_request(dst_ip)
            print result
            dic[dst_ip] = result
        i += 1
    print 'Done running'
    return dic

def is_IPv4(address):
    import socket
    try:
        socket.inet_pton(socket.AF_INET, address)
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except socket.error:
            return False
        return address.count('.') == 3
    except socket.error:  # not a valid address
        return False
    return True

import sys
if __name__ == "__main__":
    file_name = "./test/country_complete.json"

    dic = load_pickle('./test/country.json')
    dic.update(load_pickle('./test/country2.json'))
    dic.update(load_pickle('./test/country5.json'))
    dic.update(load_pickle('./test/country6.json'))
    dic.update(load_pickle('./test/country7.json'))
    save_dictionary(file_name, dic)


def old():
    file_name = "./test/country7.json"

    #netflow = load_pickle("./test/db.json")
    #print 'Loaded pickle'
    #dic = get_country(netflow, {})

    from prediction_type import PredictionFileBadSamples,PredictionFile
    data = {}
    data['from'] = 0
    data['to'] = 600000
    data['file'] = "./test/test.flow"

    #netflow = PredictionFileBadSamples().load(data, Dummy())
    #dic = get_country(netflow, {})

    data['from'] = 160000
    data['to'] = 190000
    netflow = PredictionFile().load(data, Dummy())
    dic = get_country(netflow, {})

    print dic
    save_dictionary(file_name, dic)
