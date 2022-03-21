import socket
import pickle
import sys
from helper import *

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
        self.socket = None
    
    '''
    send a simple message to the IP address 255.255.255.255 with TTL = 0
    in order to broadcast its existence
    '''
    def broadcast(self):
        self.broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            self.broad_socket.sendto(make_packet(self.ip, '255.255.255.255','', 0),
                                     ('255.255.255.255', 9999))
            recv_data, addr = self.broad_socket.recvfrom(1024)
            data = pickle.loads(recv_data)
            break
        self.broad_socket.close()
        return data
            
    def open_socket(self, dest):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((dest, 8000))
        
    '''Given a destination IP address, a text message and TTL,
    the end system will attempt to send the message through the network
    '''
    def send(self, packet):
        #msg = packet['message']
        self.socket.send(packet)
        from_server = self.socket.recv(4096)
        print(from_server.decode())

    '''
    if an end system receives a message, it should display that message
    (and any other relevant information) to its output
    '''
    def receive(self):
        pass



if __name__ == "__main__":
    host = Host(sys.argv[1], 9999)
    print("created host")
    print("Start broadcasting")
    data = host.broadcast()
    
    print("router ip: " + data['src_ip'])
    host.open_socket(data['src_ip'])
    while True:
        print("Enter message: ")
        msg = sys.stdin.readline()
        data_packet = make_packet(host.ip, "192.168.1.10", msg[:-1], 2)
        host.send(data_packet)
        if(msg[:-1] == 'exit'):
            break
    host.socket.close()
    
    