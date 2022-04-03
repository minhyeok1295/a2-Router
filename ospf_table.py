# -*- coding: utf-8 -*-
from forward_table import *
class OSPFTable(ForwardTable):
    
    def __init__(self):
        self.neighbors = {}
        super().__init__()
        
    
    #add neighbors  
    def add_neighbors(self, ip, t):
        self.neighbors[ip] = t
    
    #returns the neighbors
    def get_neighbors(self):
        return self.neighbors
    
    def check_ip(self, ip):
        if ip in self.neighbors:
            return ip, self.neighbors[ip]
        elif ip in self.table:
            return self.table[ip], self.neighbors[self.table[ip][0]]
        return None, None
    
    
    #using data sent from the monitor node, update the table and neighbors
    def update_info(self, data):
        self.neighbors = data['neighbors']
        self.table = data['table']
    
    
    #print out the table for testing purpose.
    def __str__(self):
        output = "======= Neighbors =======\n" 
        for k,v in self.neighbors.items():
            output += f"{v}\t: {k}\n"
        output += "======= Original Table =======\n" 
        output += "Destination IP\t: Next Hop IP\t Cost\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v[0]}\t {v[1]}\n"
        output += "=========================="
        return output
