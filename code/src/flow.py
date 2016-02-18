
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
        self.prtcl = self.protocol == "tcp"
        self.src_ip_num = self.ip2long(self.src_ip)
        self.dest_ip_num = self.ip2long(self.dest_ip)

        if "0x" in  str(self.src_port):
            self.src_port = int(self.src_port, 16)
        if "0x" in  str(self.dest_port):
            self.dest_port = int(self.dest_port, 16)

        if not self.src_port:
            self.src_port = 0
        if not self.dest_port:
            self.dest_port = 0

    def ip2long(self, ip):
        """
        Convert an IP string to long
        """
        import socket, struct
        try:
            packedIP = socket.inet_pton(socket.AF_INET, ip)
            return struct.unpack("!L", packedIP)[0]
        except Exception as e:
            try:
                from binascii import hexlify
                return int(hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)
            except Exception as e:
                return int(ip.replace(':', ''), 16)

    # Make a sample of this record
    def make_sample(self):
        self.make_record()
        return [self.prtcl, self.src_port, self.dest_port,
                self.src_ip_num, self.dest_ip_num, self.total_pckts,
                self.total_bytes]

    # Return the label of this record
    def make_target(self):
        return self.label
