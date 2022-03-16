import socket
import pickle
import sys
from helper import *
import threading

class Host():
    '''
    given the end system's IP addr ess, the end system will become active, open socke to its next hop connection
    and send a simple message to the IP address 255.255.255.255 with TTL=0 in order to broadcast its existence
    '''
    
    def __init__(self, ip, port):
        self.ip = ip
        self.ttl = 0
        self.next_ip = ''
        self.broad_socket = None
        self.send_sock = None
        self.thread_sock = None #listening socket: receives message from other
    
    '''
    send a simple message to the IP address 255.255.255.255 with TTL = 0
    in order to broadcast its existence
    '''
    def broadcast(self):
        self.broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.broad_socket.sendto(make_packet(self.ip, '255.255.255.255','', 0),
                                    ('255.255.255.255', 9999))
        recv_data, addr = self.broad_socket.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.broad_socket.close()
        return data
        
    def set_next_hop(self,next_hop):
        self.next_ip = next_hop

    def connect(self):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sock.connect((self.next_ip, 8000))

    '''Given a destination IP address, a text message and TTL,
    the end system will attempt to send the message through the network
    '''
    def send(self):
        while True:
            msg = input("Enter message: ")
            if(msg == 'exit'):
                exit_packet = make_packet("", "", msg, 0)
                self.connect()
                self.send_sock.send(exit_packet)
                self.send_sock.close()
                break
            else:
                dest_ip = input("Enter destination: ")
                ttl = self.get_ttl()
                if (validate_ip(dest_ip)):
                    self.connect()
                    print("send msg: " + msg + ", to dest: ", dest_ip)
                    data_packet = make_packet(self.ip, dest_ip, msg, ttl)
                    if (check_on_same_switch(self.ip, dest_ip)):
                        self.send_to_host(dest_ip, data_packet)
                    else:
                        self.send_sock.send(data_packet)
                    self.send_sock.close()
                else:
                    print("invalid ip address format")
        return 0

    def send_to_host(self, dest_ip, packet):
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.send_sock.connect((dest_ip, 8100))
        self.send_sock.send(packet)

    def open_thread_sock(self):
        self.thread_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_sock.bind((self.ip, 8100))
        self.thread_sock.listen(5)
    
    def get_ttl(self):
        invalid_ttl = True
        while invalid_ttl:
            try:
                ttl = int(input("Enter TTL: "))
                if (ttl <= 0):
                    raise
                invalid_ttl = False
            except Exception:
                print("plase enter a valid ttl")
        return ttl
    
    '''
    if an end system receives a message, it should display that message
    (and any other relevant information) to its output
    '''
    def receive(self):
        recv_sock,addr = self.thread_sock.accept()
        print(addr)
        recv_data = recv_sock.recv(4096)
        data = pickle.loads(recv_data)
        print(f"From {data['src_ip']}: {data['message']}")
        recv_sock.close()
        

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of arguments: IP address needed")
        raise
    host = Host(sys.argv[1], 9999)
    print("created host")
    print("Start broadcasting")
    broadcast_data = host.broadcast()
    
    print("router ip: " + broadcast_data['src_ip'])
    host.set_next_hop(broadcast_data['src_ip'])

    recv_t = ThreadSock(host)
    recv_t.start()
    host.send()
    print("send terminated")
    recv_t.stop()
    print("end")
    host.thread_sock.close()
    recv_t.join()
    print('Program Terminated')