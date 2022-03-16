from forward_table import * 
class RIPTbable(ForwardTable):
    
    def __init__(self,ip):
        # dest_ip : [next_hop, cost]
        super().__init__()
        self.table[ip] = [ip,0]
    
    def set_entry(self,ip,value_pair):
        self.table[ip] = value_pair
    
    def create_entry(self,ip,addr,cost):
        print("create entry is deprecated please use `set_entry`")

    def get_next_hop(self,ip):
        return self.table[ip][0]

    def __str__(self):
        output = "======= Forwarding Table =======\n"
        output += "Source IP\t: Next Hop IP\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v[0]}\tcost:{v[1]}\n"
        values = self.table.values()
        return output