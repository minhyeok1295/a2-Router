class ForwardTable:

    def __init__(self):
        # key : value => dest_ip : next_hop
        self.table = {}

    def has_ip(self,ip):
        """
        check if table has src_ip as key
        """
        return ip in self.table
    
    def create_entry(self,ip,addr,ttl=None):
        """
        add src_ip to table and the value is addr (ip of the incoming packet)
        """
        self.table[ip] = addr
    
    def get_next_hop(self,ip,addr=None,ttl=None):
        # check ttl and update here
        return self.table[ip]
    
    def _update_table(self,ip,ttl,addr):
        pass
    
    #key for each ip and value as next hop that could 
    def __str__(self):
        output = "======= Original Table =======\n"
        output += "Source IP\t: Next Hop IP\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v}\n"
        next_hop_addr = list(set(self.table.values()))
        reverse_table = {}
        output += "======= Reverse Key Value =======\n"
        for k,v in self.table.items():
            if v in reverse_table:
                reverse_table[v].append(k)
            else:
                reverse_table[v] = [k]
        for k in reverse_table.keys():
            output += f"Next Hop : {k}\n"
            for v in reverse_table[k]:
                output += f"\tDestination: {v}\n"
        return output
