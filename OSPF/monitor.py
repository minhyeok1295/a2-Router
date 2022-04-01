# -*- coding: utf-8 -*-
from router import *
from helper import *

class Monitor(Router):
    def __init__(self, ip):
        super().__init__(ip)
        
    #override
    def open_thread_sock(self):
        self.thread_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.thread_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.thread_sock.bind(('255.255.255.255',8888))
    #override
    
    def open_server(self):
        monitor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        monitor.bind((self.ip, 8000))
        monitor.listen(5)
        

        
        
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    monitor = Monitor(sys.argv[1])
    b = ThreadSock(monitor)
    b.start()
    
    print("broadcast listening")
    
    