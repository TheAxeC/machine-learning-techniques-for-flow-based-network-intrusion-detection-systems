
# The basic sniffer class
class Sniffer:

    def __init__(self):
        # Scapy variables
        self.filter = "ip"
        self.store = 0
        self.iface = "en0"

        self.tshark_cmd = "tshark -x"
        #self.tshark(self.tshark_cmd, self.pkt_tshark)

    def start(self, cmd):
        try:
            method = getattr(Sniffer, cmd)
            method(self, self.pkt_callback, self.iface, self.filter, self.store)
        except KeyboardInterrupt as e:
            pass

    # Run tshark for packet sniffing
    def tshark(self, command, action):
        for l in self.runProcess(command.split()):
            action(l)

    # Use scapy for packet sniffing
    def scapy(self, action, iface, filter, store):
        from scapy.all import sniff
        sniff(iface=iface, prn=action, filter=filter, store=store)

    # Run a process and capture the output
    def runProcess(self, exe):
        import subprocess
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return iter(p.stdout.readline, b'')

    def pkt_callback(self, pkt):
    	pkt.show() # debug statement

    def pkt_tshark(self, pkt):
        p = Packet()
        p.add_line(pkt)

class Packet:

    def __init__(self):
        self.pkt = []

    def add_line(self, line):
        # Format
        # 0340  b7 fd 2a 97 83 b9 7a b3 40 9e 93 f0 81 d7 6b 5c   ..*...z.@.....k\
        print line.split("  ")
        if len(line.split("  ")) > 1:
            self.pkt.append(line.split("  ")[1])

    def show(self):
        pass


class NetflowGenerator:

    def __init__(self):
        pass

    def add_record(self):
        pass
