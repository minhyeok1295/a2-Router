import socket
import pickle
import threading
from helper import *
from forward_table import ForwardTable

broadcast = '255.255.255.255'

def print_packet(packet):
    print("-----packet info-----")
    print("src_ip: " + packet["src_ip"])
    print("dest_ip: " + packet["dest_ip"])
    print("msg: " + packet['message'])
    print("ttl: " + str(packet['ttl']))


class Router():
    
    def __init__(self, ip):
        self.ip = ip
        self.thread_sock = None
        self.table = ForwardTable()
        self.lock = threading.Lock()

    def open_thread_sock(self):
        self.thread_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.thread_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.thread_sock.bind(('0.0.0.0',9999))

    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.lock.acquire()
        # set src ip as key, the ip where the message is coming from as value
        self.table.create_entry(data['src_ip'],addr[0])
        self.lock.release()
        self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
    
    def open_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Server connected to")
            print(addr)
            packet = conn.recv(4096)
            data = pickle.loads(packet)
            print_packet(data)
            if (data['message'] == 'exit'):
                break
            
            dest = data['dest_ip']
            self.lock.acquire()
            if self.table.has_ip(dest):
                next_hop = self.table.get_next_hop(dest)
                try:
                    self.forward(data,next_hop)
                    print(f"Successfully sent message to {data['dest_ip']}")
                except Exception:
                    print("Error!!!!")
            else:
                self.print_error(data['src_ip'],data['dest_ip'])
            self.lock.release()
            conn.close()
        conn.close()
        server.close()

    def forward(self,recv_data,next_hop):
        data =recv_data.copy()
        packet = make_packet(data['src_ip'],data['dest_ip'],data['message'],data['ttl'])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((next_hop,8100))
        sock.send(packet)
        sock.close()
    
    def print_error(self,src_ip,dest_ip):
        print("========== Error ==========")
        print(f"Bad request from {src_ip}")
        print(f"Destination {dest_ip} is unreachable\n\n")



class TableCommandThread(ThreadSock):
    def run(self):
        print("Start Command Thread")
        while not self.stopped():
            command = input()
            print("Command you entered is ",command)
            if command == "print":
                print("Executing print command")
                print(self.node.table)
        


if __name__ == "__main__":
    router = Router("10.0.0.1")
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
    #1. receive broadcast message
    #2. send packet to host who sent broadcast message
    #3. forward the message packet received to the final destination
    