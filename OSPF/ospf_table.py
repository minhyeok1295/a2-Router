# -*- coding: utf-8 -*-
class OSPFTable():
    def __init__(self):
        self.neighbors = {}
        self.table = {}
    
    def add_neighbors(self, ip, t):
        self.neighbors[ip] = t
        
    def create_entry(self, ip, addr):
        self.table[ip] = addr
    
    def get_table():
        return self.table
    
    def get_neighbors():
        return self.neighbors
    
    
    def has_ip(self,ip):
        """
        check if table has src_ip as key
        """
        return ip in self.table
    
    def check_ip(self, ip):
        mip = ip.rpartition(".")[0] + ".0"
        if ip in self.neighbors:
            return ip, self.neighbors[ip]
        elif ip in self.table:
            return self.table[ip], self.neighbors[self.table[ip]]
        elif mip in self.table:
            print("here")
            self.create_entry(ip, self.table[mip])
            return self.table[mip], "router"
        return None, None
    
    def __str__(self):
        output = "======= Neighbors =======\n" 
        for k,v in self.neighbors.items():
            output += f"{v}\t: {k}\n"
        output += "======= Original Table =======\n" 
        output += "Source IP\t: Next Hop IP\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v}\n"
        output += "=========================="
        return output
