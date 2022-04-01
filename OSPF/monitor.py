# -*- coding: utf-8 -*-
from router import *
from helper import *

class Monitor(Router):
    def __init__(self, ip):
        super().__init__(ip)
    
    def open_server(self):
        monitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        monitor.bind((self.ip, 8888))
        monitor.listen(5)
        while True:
            conn, addr = monitor.accept()
            print(addr)
            packet = conn.recv(4096)
            data = pickle.loads(packet)
            print_packet(data)
            conn.close()
        monitor.close()
        

        
        
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    monitor = Monitor(sys.argv[1])
    monitor.open_server()
    print("broadcast listening")
    
    