
class Loader:

    @staticmethod
    def get_loader(name, default=None):
        import sys

        try:
            return getattr(sys.modules[__name__], name)()
        except Exception as e:
            print "Loader \"" + name + "\"does not exist."
            return default

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
    def load(self, file_name, fr, to, good_labels=None, good=True):
        try:
            with open(file_name) as f:
                next(f)

                i = 0
                while i < fr and next(f):
                    i += 1

                for line in f:
                    items = line.split(',')
                    item = self.load_single(items)

                    if good_labels:
                        if good:
                            if item.make_target() in good_labels:
                                self.flow.add_record(item)
                        else:
                            if not item.make_target() in good_labels:
                                self.flow.add_record(item)
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

class SQLLoader:
    def __init__(self):
        from flow import Flows
        self.flow = Flows()
        self.cmd = "SELECT * FROM `flows` ORDER BY RAND() LIMIT %s"
        self.cmd_good = "SELECT * FROM `flows` WHERE `id` NOT IN (SELECT `flowid` FROM `flow_alert`) ORDER BY RAND() LIMIT %s"

    # Load a file
    def load(self, host, user, password, db, amount, good=False):
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
                if good:
                    cursor.execute(self.cmd_good, (amount,))
                else:
                    cursor.execute(self.cmd, (amount,))

                for row in cursor:
                    item = self.load_single(row, good)
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
    def load_single(self, items, good):
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
        if good:
            rec.label = 'non-malicous'
        else:
            rec.label = 'malicous'
        rec.tcp_flags = items['tcp_flags']
        return rec

    # Get the netflow
    def get_netflow(self):
        return self.flow
