
class Interface:
    """
    Stores the interface information.
    Assume prefix bits are in {8,16,24}
    """

    def __init__(self,ip,prefix):
        self.ip = ip    # the ip on the router side
        assert(prefix in [8,16,24],"Got invalid interface prefix")
        self.prefix = prefix    # number of interface prefix bits
        self.interface = self.calc_interface(ip,prefix)     # interface

    def calc_interface(self,ip,prefix):
        ip_bits = ip.split(".")
        print(ip_bits)
        assert(len(ip_bits)==4)
        if prefix == 8:
            return '.'.join(ip_bits[0])
        elif prefix == 16:
            return '.'.join(ip_bits[:2])
        else:
            return '.'.join(ip_bits[:3])

    def __eq__(self,other):
        if isinstance(other,Interface):
            return self.interface == other.interface
        if type(other) == str:
            return self.interface == other
        return False
    
    def __repr__(self):
        return self.ip+"/"+self.prefix