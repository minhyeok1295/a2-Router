# -*- coding: utf-8 -*-
from router import *
from helper import *
from dijkstra import *
import time

class Monitor(Router):
    def __init__(self, ip):
        super().__init__(ip)
        self.network = {}
        self.routers = []
        self.total_time = 0
        self.num = 0
        
    #disconnect router with "ip" from all other routers that are connected    
    def disconnect_from_network(self, ip):
        for router in self.network:
            if (self.network[router].get(ip, False) != False):
                self.network[router].pop(ip)
            if router == ip:
                self.network[router] = {k:v for k,v in self.network[router].items() if v[0] != "router"}
    
    def open_server(self):
        monitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        monitor.bind((self.ip, 8888))
        monitor.listen(5)
        while True:
            conn, addr = monitor.accept()
            packet = conn.recv(4096)
            data = pickle.loads(packet) 
            src_ip = data['src_ip']
            dst_ip = data['dest_ip']
            if (len(data) == 5): #table packet
                self.network[src_ip][dst_ip] = ('router', 1)
                self.network[dst_ip][src_ip] = ('router', 1)
                self.update_tables()
            else:
                if (data['message'] == 'router'): #router added
                    self.network[src_ip] = {}
                    self.routers.append(src_ip)
                elif (data['message'] == 'host'): #host added
                    self.network[dst_ip][src_ip] = ("host", 1)
                    self.update_tables()
                elif (data['message'] == 'disconnect'): #disconnect router.
                    self.disconnect_from_network(src_ip)
                    self.update_tables()
            conn.close()
        monitor.close()
        
    #send the updated table back to router.
    def send_table(self, ip, table, neighbors):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 8000))
        s.send(make_table_packet(None, ip, table, neighbors))
        s.close()
        
    #update the table in the monitor node using dijkstra algorithm in dijkstra.py    
    def update_tables(self):
        start = time.time()
        for router in self.routers:
            neighbors = {}
            for k,v in self.network[router].items(): #get all neighbors in a new dic.
                neighbors[k] = v[0]
            table = update_table(self.network, self.routers, router) #FUNCTION IN dijkstra.py
            self.send_table(router, table, neighbors)
        end = time.time()
        print("time: " + str(end - start))
        self.total_time += (end - start)
        self.num += 1
                  
    #print out the list of routers and all connected neighbors for each of them.        
    def print_network(self):
        output = "==================\n"
        for k,v  in self.network.items():
            output += f"{k}\t: {v}\n"
        output += "==================\n"
        print(output)

class TableCommandThread(ThreadSock):
    def run(self):
        print("Start Command Thread")
        while not self.stopped():
            command = input()
            if command == "print":
                self.node.print_network()
            if command == "time":
                print(self.node.total_time / self.node.num)
            
        
        
if __name__ == "__main__":
    monitor = Monitor("10.0.0.1")
    
    command_t = TableCommandThread(monitor)
    command_t.start()
    monitor.open_server()
    
    command_t.stop()
    print("broadcast listening")
    
    