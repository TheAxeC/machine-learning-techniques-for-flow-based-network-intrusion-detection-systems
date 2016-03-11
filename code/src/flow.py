
# A list of flows
class Flows:

    def __init__(self):
        self.netflow = []
        self.flow_sample_data = []
        self.flow_targets = []

    def add_record(self, item):
        self.netflow.append(item)
        self.flow_sample_data.append(item.make_sample())
        self.flow_targets.append(item.make_target())

    # Get the netflow
    def get_netflow(self):
        return self.netflow

    # Get the sampled data
    def get_sample_data(self):
        return self.flow_sample_data

    # Get the sampled data
    def get_raw_data(self):
        l = []
        for i in self.netflow:
            l.append(i.make_raw())
        return l

    # Get the targets (labels)
    def get_target_data(self):
        return self.flow_targets

    # Get the sample size
    def get_size(self):
        return len(self.netflow)


# A flow record
class FlowRecord:

    # Init basic variables
    def __init__(self):
        # Timing
        self.start_time = 0
        self.duration = 0

        # Protocols
        self.protocol = 0
        self.src_port = 0
        self.dest_port = 0
        self.src_ip = 0
        self.dest_ip = 0

        # bidirectional flow?
        self.bidirectional = 0

        self.state = 0
        self.sTos = 0
        self.dTos = 0

        self.total_pckts = 0
        self.total_bytes = 0
        self.total_srcbytes = 0

        self.label = 0

    def make_record(self):
        self.prtcl = abs(hash(str(self.protocol))) % (10 ** 8)

        self.src_ip_num =  abs(hash(str(self.src_ip))) % (10 ** 8)
        self.dest_ip_num =  abs(hash(str(self.dest_ip))) % (10 ** 8)

        if "0x" in  str(self.src_port):
            self.src_port = int(self.src_port, 16)
        if "0x" in  str(self.dest_port):
            self.dest_port = int(self.dest_port, 16)

        if not self.src_port:
            self.src_port = 0
        if not self.dest_port:
            self.dest_port = 0

        self.sTos = abs(hash(str(self.sTos))) % (10 ** 8)
        self.dTos = abs(hash(str(self.dTos))) % (10 ** 8)
        self.state = abs(hash(str(self.state))) % (10 ** 8)

        if self.bidirectional == "->":
            self.dir = 0
        elif self.bidirectional == '<-':
            self.dir = 1
        else:
            self.dir = 2

        #from geoipc import GeoIP
        #gi = GeoIP('GeoIP.dat')
        #try:
        #    self.cntry1 = abs(hash(str(gi.country(self.src_ip)))) % (10 ** 8)
        #except:
        #    self.cntry1 = 0
        #try:
        #    self.cntry2 = abs(hash(str(gi.country(self.dest_ip)))) % (10 ** 8)
        #except:
        #    self.cntry2 = 0


    # Make a sample of this record
    def make_sample(self):
        self.make_record()
        return [int(self.prtcl), int(self.src_port), int(self.dest_port),
                int(self.sTos), int(self.dTos), int(self.state), int(self.total_srcbytes),
                float(self.duration), int(self.src_ip_num) , int(self.dest_ip_num),
                int(self.total_pckts), int(self.total_bytes)] #, int(self.cntry1), int(self.cntry2)]

    def make_raw(self):
        return {
                    "protocol":str(self.protocol),
                    "src_port":str(self.src_port),
                    "dest_port":str(self.dest_port),
                    "srcbytes":int(self.total_srcbytes),
                    "duration":float(self.duration),
                    "src_ip":str(self.src_ip) ,
                    "dest_ip":str(self.dest_ip),
                    "totalpackets":int(self.total_pckts),
                    "totalbytes":int(self.total_bytes)
                }

    # Return the label of this record
    def make_target(self):
        return self.label
