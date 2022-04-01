# -*- coding: utf-8 -*-
from router import *
from helper import *

class Node:
    def __init__(self, ip):
        self.ip = ip
        self.hosts = []



class Monitor(Router):
    def __init__(self, ip):
        super().__init__(ip)
        self.routers = {}
    
    def open_server(self):
        monitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        monitor.bind((self.ip, 8888))
        monitor.listen(5)
        while True:
            conn, addr = monitor.accept()
            print(addr)
            packet = conn.recv(4096)
            data = pickle.loads(packet)
            
            if (data['message'] == 'router'): #router added
                self.routers['src_ip'] = Node(data['src_ip'])
            elif (data['message'] == 'host'): #host added
                self.routers['dst_ip'].hosts.append(data['src_ip'])
            conn.close()
        monitor.close()
        

        
        
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    monitor = Monitor(sys.argv[1])
    monitor.open_server()
    print("broadcast listening")
    
    