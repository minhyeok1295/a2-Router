# -*- coding: utf-8 -*-
class OSPFTable():
    
    def __init__(self):
        self.neighbors = {}
        self.table = {}
        
    
    #add neighbors  
    def add_neighbors(self, ip, t):
        self.neighbors[ip] = t
        
    #add entry in the OSPF table    
    def create_entry(self, ip, addr):
        self.table[ip] = addr
    
    #returns the table
    def get_table(self):
        return self.table
    
    #returns the neighbors
    def get_neighbors(self):
        return self.neighbors
    
    
    def has_ip(self,ip):
        """
        check if table has src_ip as key
        """
        return ip in self.table
    
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
