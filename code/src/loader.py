

# Load a netflow file
class NetflowLoader:

    def __init__(self):
        from flow import Flows
        self.flow = Flows()
        self.loaded_file = None

    # Get the file size
    def get_file_size(self, file_name):
        try:
            return sum(1 for line in open(file_name))
        except Exception as e:
            return -1

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
