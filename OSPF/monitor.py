# -*- coding: utf-8 -*-
from router import *
from helper import *
from dijkstra import *


class Monitor(Router):
    def __init__(self, ip):
        super().__init__(ip)
        self.network = {}
        self.routers = []
        
    
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
            conn.close()
        monitor.close()
        
    def send_table(self, ip, table, neighbors):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 8000))
        s.send(make_table_packet(ip, table, neighbors))
        s.close()
        
    def update_tables(self):
        for router in self.routers:
            neighbors = {}
            for k,v in self.network[router].items():
                neighbors[k] = v[0]
            table = update_table(self.network, self.routers, router)
            self.send_table(router, table, neighbors)
                  
            
            
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
            print("Command you entered is ",command)
            if command == "print":
                print("Executing print command")
                self.node.print_network()
                print(self.node.routers)
            
        
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    monitor = Monitor(sys.argv[1])
    
    command_t = TableCommandThread(monitor)
    command_t.start()
    monitor.open_server()
    
    command_t.stop()
    print("broadcast listening")
    
    