# -*- coding: utf-8 -*-
from forward_table import *

class OSPFTable(ForwardTable):
    def __init__(self):
        super().__init__()
        self.neighbors = {}
        self.table = {}
        
    def add_neighbors(self, ip, t):
        self.neighbors[ip] = t
   
    def __str__(self):
        output = "======= Neighbors =======\n" 
        for n in self.neighbors:
            output += f"{n}\n"
