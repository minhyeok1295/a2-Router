from router import *
from helper import *
from ospf_table import *
import sys
import time
class OSPFRouter(Router):
    def __init__(self, ip):
        super().__init__(ip)
        self.table = OSPFTable()
    
    #receive 
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        if (check_on_same_switch(self.ip, data['src_ip'])):
            self.notify_monitor_new_host(data['src_ip'])
            self.lock.acquire()
            # set src ip as key, the ip where the message is coming from as value 
            self.table.create_entry( data['src_ip'], addr[0])
            self.table.add_neighbors(data['src_ip'], "host")
            self.lock.release()
            self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
        else: #it is router
            self.thread_sock.sendto(make_packet(self.ip,addr,'NA',0),addr)
    
    #connect to monitor
    def connect_to_monitor(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.1", 8888))
        return s
    
    #notify the monitor node that the router has been connected to the given ip.
    def notify_monitor_connect(self, ip):
        s = self.connect_to_monitor()
        s.send(make_table_packet(self.ip, ip, self.table, {}))
        s.close()

    #notify the monitor node that new router has been added    
    def notify_monitor_new_router(self):
        s = self.connect_to_monitor()
        s.send(make_packet(self.ip, "10.0.0.1", "router", 0))
        s.close()
        
    #notify the monitor node that new host has been added    
    def notify_monitor_new_host(self, ip):
        s = self.connect_to_monitor()
        s.send(make_packet(ip, self.ip, "host", 0))
        s.close()
        
    def notify_monitor_disconnect(self):
        s = self.connect_to_monitor()
        s.send(make_packet(self.ip, "10.0.0.1", "disconnect", 0))
        s.close()
        
   
    
    #decrement 1 ttl and forward message to next hop if it is possible. Drop packet
    #if its not possible.
    def handle_message_packet(self, data):
        data['ttl'] -= 1
        if (data['ttl'] > 0):
            dest = data['dest_ip']
            self.lock.acquire()
            next_hop, t = self.table.check_ip(dest)
            if next_hop != None:
                try:
                    if (isinstance(next_hop, list)):
                        self.forward(data,next_hop[0], t)
                        print(f"Successfully sent message to {t}, {next_hop[0]}")
                    else:
                        self.forward(data, next_hop, t)
                        print(f"Successfully sent message to {t}, {next_hop}")
                except Exception:
                    print("Error!!!!")
                self.lock.release() 
            else:
                print_error(data['src_ip'],data['dest_ip'])
                self.lock.release()
        else:
            print_ttl_expired(self.ip,data)    
        
    #open up the server for router.    
    def open_server(self):
        self.notify_monitor_new_router()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            packet = conn.recv(4096)
            if len(packet) != 0:
                data = pickle.loads(packet)
                if (len(data) == 5): #updating table
                    self.lock.acquire()
                    self.table.update_info(data)
                    self.lock.release()
                    #print("updated table")
                else:
                    if (data['message'] == 'exit'):
                        break
                    self.handle_message_packet(data)
            else:
                print("nothing received")
            conn.close()
        conn.close()
        server.close()
    
    #forward the received data to next hop port 8100: host, 8000: router
    def forward(self,recv_data, next_hop, tp):
        data = recv_data.copy()
        packet = make_packet(data['src_ip'],data['dest_ip'],data['message'],data['ttl']) 
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if (tp == "host"):
            sock.connect((next_hop,8100))
        else: #forward to router
            sock.connect((next_hop,8000))
        sock.send(packet)
        sock.close()
        

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    router = OSPFRouter(sys.argv[1])
    broadcast_t = ThreadSock(router)
    command_t = TableCommandThread(router)
    broadcast_t.start()
    command_t.start()
    router.open_server()
    broadcast_t.stop()
    command_t.stop()
    router.thread_sock.close()
    broadcast_t.join()
    command_t.join()