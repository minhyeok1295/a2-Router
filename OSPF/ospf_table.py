# -*- coding: utf-8 -*-
class OSPFTable():
    def __init__(self):
        self.neighbors = {}
        self.table = {}
        
    def create_entry(self, ip, addr, t):
        self.neighbors[ip] = t
        print(self.neighbors)
        self.table[ip] = addr
   
    def __str__(self):
        output = "======= Neighbors =======\n" 
        for k,v in self.neighbors:
            output += f"{v}\t: {k}\n"
        output = "======= Original Table =======\n" 
        output += "Source IP\t: Next Hop IP\n"
        for k,v in self.table.items():
            output += f"{k}\t: {v}\n"
        return output
