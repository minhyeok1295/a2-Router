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
        #self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.socket.connect((self.next_ip, 9999))
    
    '''   
    def make_packet(self, src_ip, dest_ip, message, ttl):
        data = {
            'src_ip' : src_ip,
            'dest_ip' : dest_ip,
            'message' : message,
            'ttl' : ttl
        }
        return pickle.dumps(data)
     '''   
    
    '''
    send a simple message to the IP address 255.255.255.255 with TTL = 0
    in order to broadcast its existence
    '''
    def broadcast(self):
        self.broad_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.broad_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            self.broad_socket.sendto(make_packet(self.ip, '255.255.255.255','', 0), ('255.255.255.255', 9999))
            recv_data, addr = self.broad_socket.recvfrom(1024)
            data = pickle.loads(recv_data)
            break
        self.broad_socket.close()
        return data
            
        
    '''Given a destination IP address, a text message and TTL,
    the end system will attempt to send the message through the network
    '''
    def send(self, dest_ip, message, ttl):
        pass
    
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
    
    print(data['src_ip'])
    print(data['dest_ip'])
    
    
    