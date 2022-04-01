# -*- coding: utf-8 -*-
class OSPFTable():
    def __init__(self):
        self.neighbors = {}
        self.table = {}
    
    def add_neighbors(self, ip, t):
        self.neighbors[ip] = t
        
    def create_entry(self, ip, addr):
        self.table[ip] = addr
    
    def has_ip(self,ip):
        """
        check if table has src_ip as key
        """
        return ip in self.table
   
    def __str__(self):
        output = "======= Neighbors =======\n" 
        for k,v in self.neighbors.items():
            output += f"{v}\t: {k}\n"
        output += "======= Original Table =======\n" 
        output += "Source IP\t: Next Hop IP\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v}\n"
        return output
