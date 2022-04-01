# -*- coding: utf-8 -*-
from router import *
from helper import *
class Monitor(Router):
    def __init__(self, ip):
        super.__init__(ip)
    
    
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        print_packet(data)
        if (check_on_same_switch(self.ip, data['src_ip'])):
            self.lock.acquire()
            # set src ip as key, the ip where the message is coming from as value
            self.table.create_entry(data['src_ip'],addr[0])
            self.lock.release()
            self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
        else: #it is router
            self.thread_sock.sendto(make_packet(self.ip,addr,'NA',0),addr)

        
        
        
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    monitor = Monitor(sys.argv[1])
    broadcast_t = ThreadSock(monitor)
    broadcast_t.start()
    