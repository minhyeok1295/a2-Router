import socket
import pickle
import threading
from helper import *
from forward_table import ForwardTable

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
        self.thread_sock.bind(('0.0.0.0',9999))
        
    def receive(self):
        pass
    
    def forward(self):
        pass
    
    def open_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Server connected to")
            print(addr)
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
    