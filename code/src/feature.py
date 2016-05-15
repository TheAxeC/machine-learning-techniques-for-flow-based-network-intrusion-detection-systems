
class BasicFeature:

    def __init__(self):
        pass

    @staticmethod
    def get_feature(name, file):
        import sys

        try:
            return getattr(sys.modules[__name__], name)(file)
        except Exception as e:
            print "Feature \"" + str(name) + "\" does not exist."
            return None

# A class to construct the feature from raw flow data
class FlowFeature(BasicFeature):

    # Initialisation
    def __init__(self, file):
        self.read_config(file)

    # Reading the config file
    def read_config(self, file=None):
        import json

        try:
            file_name = None
            if file:
                file_name = file
            else:
                file_name = self.default

            with open(file_name) as data_file:
                data = json.load(data_file)
                if "protocols" in data:
                    self.protocols = data["protocols"]
            return True
        except Exception as e:
            print e
            print self.data
            return False

    # Get the protocol into a feature (index in self.protocols)
    def get_protocol_feature(self, protocol):
        prot = [0] * (len(self.protocols)+1)
        try:
            #prot[self.protocols.index(protocol)] = 1
            for i in self.protocols:
                if protocol in i:
                    prot[self.protocols.index(i)] = 1
        except ValueError:
            prot[ len(self.protocols) ] = 1
        return prot

    # Get the feature for the port
    # If the port is normal behaviour (in self.ports) for the given protocol,
    # 1 is returned
    # Otherwise, 0 is returned
    def get_port_feature(self, port):
        try:
            port = int(port)
        except Exception as e:
            try:
                port = int(port, 16)
            except Exception as e:
                port = 0

        return port < 1024
        #if protocol.lower() in self.ports:
        #    return port in self.ports[protocol.lower()]
        #else:
        #    return port in self.ports["other"]

    # Check if a string is an IPv4 address
    # Source: http://stackoverflow.com/questions/319279/how-to-validate-ip-address-in-python
    def is_IPv4(self, address):
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

    # Check if a string is an IPv6 address
    def is_IPv6(self, address):
        import socket
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True

    # Check if a string is an MAC address
    # Source: http://stackoverflow.com/questions/7629643/how-do-i-validate-the-format-of-a-mac-address
    def is_MAC(self, address):
        import re
        return re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", address.lower())

    def get_IPv4(self, address):
        import socket
        if self.is_IPv4(address):
            return int(socket.inet_aton(address).encode('hex'),16)
        else:
            return 0

    def get_IPv6(self, address):
        import socket
        if self.is_IPv6(address):
            return int(socket.inet_pton(socket.AF_INET6, address).encode('hex'),16)
        else:
            return 0

    def get_MAC(self, address):
        if self.is_MAC(address):
            return int(address.replace(':', ''), 16)
        else:
            return 0

    def print_record(self, arr):
        print "----------------------------"
        print "record: "
        print "[protocol, src_port, dst_port, srcbytes, duration, src_ip, dst_ip, packets, bytes]"
        print arr
        print "----------------------------"
        print "end record"

    def make_record(self, flow):
        #self.print_record(flow)
        arr = [
                    int(self.get_port_feature(flow.src_port)),
                    int(self.get_port_feature(flow.dest_port)),
                    float(flow.duration),
                    int(self.get_IPv4(flow.src_ip)) ,
                    int(self.get_IPv6(flow.src_ip)) ,
                    int(self.get_MAC(flow.src_ip)) ,
                    int(self.get_IPv4(flow.dest_ip)) ,
                    int(self.get_IPv6(flow.dest_ip)) ,
                    int(self.get_MAC(flow.dest_ip)) ,
                    int(flow.total_pckts),
                    int(flow.total_bytes),
                    #int(flow.tcp_flags)
                ]
        arr.extend( self.get_protocol_feature(flow.protocol) )
        return arr
