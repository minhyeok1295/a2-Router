from forward_table import * 
class RIPTable(ForwardTable):
    
    def __init__(self):
        # dest_ip : [next_hop,interface_ip, cost]
        super().__init__()
    
    def set_entry(self,ip,value_pair):
        self.table[ip] = value_pair
    
    def create_entry(self,ip,addr,cost):
        print("create entry is deprecated please use `set_entry`")

    def get_next_hop(self,ip):
        return self.table[ip]

    def __str__(self):
        output = "======= Forwarding Table =======\n"
        output += "Source IP\t: Next Hop IP\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v[0]}\tinterface:{v[1]}\tcost:{v[2]}\n"
        values = self.table.values()
        return output