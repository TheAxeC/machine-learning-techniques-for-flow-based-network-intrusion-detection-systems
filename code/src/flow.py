
# A list of flows
class Flows:

    def __init__(self):
        self.netflow = []
        self.flow_targets = []

    def add_record(self, item):
        self.netflow.append(item)
        self.flow_targets.append(item.make_target())

    # Get the netflow
    def get_netflow(self):
        return self.netflow

    # Get the sampled data
    def get_sample_data_complete(self, feature):
        l = []
        for i in self.netflow:
            l.append(feature.make_record(i))
        return l

    # Get the sampled data
    def get_sample_data(self, feature, i):
        return feature.make_record(self.netflow[i])

    # Get the targets (labels)
    def get_target_data(self):
        return self.flow_targets

    # Get the sample size
    def get_size(self):
        return len(self.netflow)

    def addFlows(self, flows):
        self.netflow = self.netflow + flows.netflow
        self.flow_targets = self.flow_targets + flows.flow_targets

    def random(self, amount=-1):
        import random
        if amount < 0:
            amount = len(self.netflow)
        sample = random.sample(self.netflow, amount)

        newFlow = Flows()
        newFlow.netflow = sample
        newFlow.flow_targets = []
        for item in newFlow.netflow:
            newFlow.flow_targets.append(item.make_target())
        return newFlow

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
        self.tcp_flags = 0

        self.label = 0
        self.prediction = ""

    # Get the sampled data
    def get_sample_data(self, feature):
        return feature.make_record(self)

    # Return the label of this record
    def make_target(self):
        return self.label
