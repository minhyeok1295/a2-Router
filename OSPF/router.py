import socket
import pickle
import threading
from helper import *
from forward_table import ForwardTable
import sys
broadcast = '255.255.255.255'


class Router():
    
    def __init__(self, ip):
        self.ip = ip
        self.thread_sock = None
        self.table = ForwardTable()
        self.lock = threading.Lock()

    def open_thread_sock(self):
        self.thread_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.thread_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.thread_sock.bind(('255.255.255.255',9999))
    
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        if (check_on_same_switch(self.ip, data['src_ip'])):
            self.lock.acquire()
            # set src ip as key, the ip where the message is coming from as value
            self.table.create_entry(data['src_ip'],addr[0])
            self.lock.release()
            self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
        else: #it is router
            self.thread_sock.sendto(make_packet(self.ip,addr,'NA',0),addr)
            
    def notify_monitor_new_router(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.1", 8888))
        s.send(make_packet(self.ip, "10.0.0.1", "router", 0))
        s.close()
        
    def notify_monitor_new_host(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.1", 8888))
        s.send(make_packet(ip, self.ip, "host", 0))
        s.close()
    
    def open_server(self):
        self.notify_monitor_new_router()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Server connected to")
            print(addr)
            self.notify_monitor_new_host()
            packet = conn.recv(4096)
            if len(packet) != 0:
                data = pickle.loads(packet)
                print_packet(data)
                if (data['message'] == 'exit'):
                    break
                data['ttl'] -= 1
                if (data['ttl'] > 0):
                    dest = data['dest_ip']
                    self.lock.acquire()
                    if self.table.has_ip(dest):
                        next_hop = self.table.get_next_hop(dest)
                        print(next_hop)
                        try:
                            self.forward(data,next_hop)
                            print(f"Successfully sent message to {data['dest_ip']}")
                        except Exception:
                            print("Error!!!!")
                    else:
                        print_error(data['src_ip'],data['dest_ip'])
                    self.lock.release()
                else:
                    print_ttl_expired(self.ip,data['src_ip'],data['dest_ip'])
            else:
                print("nothing received")
            conn.close()
        conn.close()
        server.close()

    def forward(self,recv_data, next_hop):
        data =recv_data.copy()
        packet = make_packet(data['src_ip'],data['dest_ip'],data['message'],data['ttl'])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((next_hop,8100))
        sock.send(packet)
        sock.close()


class TableCommandThread(ThreadSock):
    def run(self):
        print("Start Command Thread")
        while not self.stopped():
            command = input()
            print("Command you entered is ",command)
            if command == "print":
                print("Executing print command")
                print(self.node.table)
            if command == "print2":
                self.node.table.print2()
        


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    router = Router(sys.argv[1])
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
    