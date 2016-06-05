
class Loader:

    @staticmethod
    def get_loader(name, default=None):
        import sys

        try:
            return getattr(sys.modules[__name__], name)()
        except Exception as e:
            print "Loader \"" + name + "\"does not exist."
            return default

    data = {}

    @staticmethod
    def get_data(name):
        if name in Loader.data:
            return Loader.data[name]
        return None

    @staticmethod
    def insert_data(name, content):
        Loader.data[name] = content
        return content

# Load a netflow file
class CTULoader:

    def __init__(self):
        from flow import Flows
        self.flow = Flows()

    # Get the labels used
    def get_labels(self, file_name):
        labels = {}
        try:
            with open(file_name) as f:
                next(f)
                for line in f:
                    items = line.split(',')
                    labels[items[14].strip()] = True
        except Exception as e:
            return []
        return labels.keys()

    # Load a file
    def load(self, file_name, fr, to, good_labels=None, good=True, amount=-1, amountGood=0):
        f = Loader.get_data(file_name)
        if not f:
            f = open(file_name)
            Loader.insert_data(file_name, f)
            print 'Loaded data manually'
        else:
            print 'Use stored data'
        f.seek(0,0)
        try:
            next(f)

            i = 0
            total = 0
            while i < fr and next(f):
                i += 1

            g = 0
            for line in f:
                if amount >= 0 and total >= amount:
                    if g >= amountGood:
                        break

                items = line.split(',')
                item = self.load_single(items)

                if good_labels:
                    if good:
                        if item.make_target() in good_labels:
                            total += 1
                            self.flow.add_record(item)
                    else:
                        if not item.make_target() in good_labels:
                            if total <= amount or amount == -1:
                                total += 1
                                self.flow.add_record(item)
                        elif g < amountGood:
                            self.flow.add_record(item)
                            g += 1
                else:
                    self.flow.add_record(item)

                if i == to:
                    break
                i += 1

            return True
        except Exception as e:
            return False

    # Load a single line
    # Format:
    #   StartTime,Dur,Proto,SrcAddr,Sport,Dir,DstAddr,Dport,State,sTos,dTos,TotPkts,TotBytes,SrcBytes,label
    #   2011/08/10 09:46:59.607825,1.026539,tcp,94.44.127.113,1577,   ->,147.32.84.59,6881,S_RA,0,0,4,276,156,flow=Background-Established-cmpgw-CVUT
    def load_single(self, items):
        from flow import FlowRecord
        rec = FlowRecord()
        rec.start_time = items[0].strip()
        rec.duration = items[1].strip()
        rec.protocol = items[2].strip()
        rec.src_ip = items[3].strip()
        rec.src_port = items[4].strip()
        rec.bidirectional = items[5].strip()
        rec.dest_ip = items[6].strip()
        rec.dest_port = items[7].strip()
        rec.state = items[8].strip()
        rec.sTos = items[9].strip()
        rec.dTos = items[10].strip()
        rec.total_pckts = items[11].strip()
        rec.total_bytes = items[12].strip()
        rec.total_srcbytes = items[13].strip()
        rec.label = items[14].strip()
        return rec

    # Get the netflow
    def get_netflow(self):
        return self.flow

class PickleLoader:
    def __init__(self):
        from flow import Flows
        self.flow = Flows()

    # Get the netflow
    def get_netflow(self):
        return self.flow

    # Load a file
    def load(self, host, user, password, db, amount, good=False, classify=False, db_file=""):
        file_name = db_file

        try:
            self.flow = Loader.get_data(file_name)
            if not self.flow:
                import pickle
                self.flow = pickle.load( open( file_name, "r+" ) )
                Loader.insert_data(file_name, self.flow)
                print 'Loaded data manually'
            else:
                print 'Use stored data'

            self.flow = self.flow.random(amount)
            return True
        except Exception as e:
            return False

class SQLLoader:
    def __init__(self):
        from flow import Flows
        self.flow = Flows()
        self.cmd = "SELECT * FROM `flows` LIMIT %s, %s"
        self.cmd_total = "SELECT * FROM `flows` INNER JOIN `flow_alert` ON flows.id = flow_alert.flowid INNER JOIN `alerts` ON flow_alert.alertid = alerts.id INNER JOIN `alert_type` ON alerts.type = alert_type.id LIMIT %s, %s"
        self.cmd_good = "SELECT * FROM `flows` WHERE `id` NOT IN (SELECT `flowid` FROM `flow_alert`) LIMIT %s, %s"

    # Load a file
    def load(self, host, user, password, db, amount, good=False, classify=False):
        import pymysql.cursors

        # Connect to the database
        connection = pymysql.connect(host=host,
                                     user=user,
                                     password=password,
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                import random
                size = 14164163
                ran = random.randint(0, size-amount)
                if classify:
                    cursor.execute(self.cmd_total, (ran, amount,))
                elif good:
                    cursor.execute(self.cmd_good, (ran, amount,))
                else:
                    cursor.execute(self.cmd, (ran, amount,))

                for row in cursor:
                    item = self.load_single(row, good, classify)
                    self.flow.add_record(item)

                ret = True
        except Exception as e:
            print "Error: " + str(e)
            ret = False
        finally:
            connection.close()
        return ret

    # Load a single line
    # Format:
    #   StartTime,Dur,Proto,SrcAddr,Sport,Dir,DstAddr,Dport,State,sTos,dTos,TotPkts,TotBytes,SrcBytes,label
    #   2011/08/10 09:46:59.607825,1.026539,tcp,94.44.127.113,1577,   ->,147.32.84.59,6881,S_RA,0,0,4,276,156,flow=Background-Established-cmpgw-CVUT
    def load_single(self, items, good, classify):
        import socket, ipaddress
        from flow import FlowRecord
        rec = FlowRecord()
        rec.start_time = items['start_time']
        rec.duration = (items['start_time'] + items['start_msec']/1000.0) - (items['end_time'] + items['end_msec']/1000.0)
        rec.protocol = items['prot']
        rec.src_ip = str(ipaddress.ip_address(items['src_ip']))
        rec.src_port = items['src_port']
        rec.dest_ip = str(ipaddress.ip_address(items['dst_ip']))
        rec.dest_port = items['dst_port']
        rec.total_pckts = items['packets']
        rec.total_bytes = items['octets']

        if classify:
            rec.label = items['description']
        elif good:
            rec.label = 'non-malicous'
        else:
            rec.label = 'malicous'
        rec.tcp_flags = items['tcp_flags']
        return rec

    # Get the netflow
    def get_netflow(self):
        return self.flow

class BinaryLoader:

    # Load a file
    def load(self, filepath, amount, predictor):

        try:
            import pynfdump_src
            d=pynfdump_src.search_file(filepath)

            i = 0
            for r in d:
                if amount >= 0 and i >= amount:
                    break
                if i % 100 == 0:
                    print "Computed " + str(i) + " flows..."
                i += 1
                flow = self.load_single(r)
                predictor.predict_flow(flow)
            print "Done predicting elements from NFDump."
            print str(amount) + " element predicted."
            print "Waiting for KeyboardInterrupt..."
        except KeyboardInterrupt as e:
            pass
        return True

    # Load a single line
    def load_single(self, items):
        import socket, ipaddress
        from flow import FlowRecord
        rec = FlowRecord()

        import datetime
        start = (items['first']-datetime.datetime(1970,1,1)).total_seconds()
        end = (items['last']-datetime.datetime(1970,1,1)).total_seconds()

        rec.start_time = start
        rec.duration = -1 * ((start + items['msec_first']/1000.0) - (end + items['msec_last']/1000.0))
        rec.protocol = items['prot']
        rec.src_ip = str(items['srcip'])
        rec.src_port = items['srcport']
        rec.dest_ip = str(items['dstip'])
        rec.dest_port = items['dstport']
        rec.total_pckts = items['packets']
        rec.total_bytes = items['bytes']

        rec.label = "Unknown"

        return rec

    # Get the netflow
    def get_netflow(self):
        return None
