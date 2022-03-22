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
        self.socket = None
        self.recv_sock = None
    
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
            
    def open_socket(self, dest):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((dest, 8000))
        while True:
            msg = input("Enter Message: ")
            dest = input("Enter destination IP: ")
            print("send to " + dest + ",msg: " + msg)
            data_packet = make_packet(self.ip, dest, msg, 2)
            self.send(data_packet)
            if(msg[:-1] == 'exit'):
                break
            self.socket.close()
            
        
    '''Given a destination IP address, a text message and TTL,
    the end system will attempt to send the message through the network
    '''
    def send(self, packet):
        #msg = packet['message']
        self.socket.send(packet)
        from_server = self.socket.recv(4096)
        print(from_server.decode())

    def open_recv_sock(self):
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_sock.bind((self.ip, 8100))
        self.recv_sock.listen(5)
    
    def wait_for_message(self):
        packet = self.recv_sock.recv(4096)
        data = pickle.loads(packet)
        print("msg: " + data['message'])
        print("from: " + data['src_ip'])
    
    def close_recv_sock(self):
        self.recv_sock.close()
        
    '''
    if an end system receives a message, it should display that message
    (and any other relevant information) to its output
    '''
    def receive(self):
        pass

class RecvSockThread(threading.Thread):
    
    def __init__(self,host):
        threading.Thread.__init__(self)
        self.host = host
        # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        self._stop_event = threading.Event()
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.host.open_recv_sock()
        while not self.stopped():
            self.host.wait_for_message()
        self.host.close_recv_sock()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of arguments: IP address needed")
        raise
    host = Host(sys.argv[1], 9999)
    print("created host")
    recv_sock = RecvSockThread(host)
    recv_sock.start()
    print("Start broadcasting")
    data = host.broadcast()
    
    print("router ip: " + data['src_ip'])
    host.open_socket(data['src_ip'])
    while not recv_sock.stopped():
        recv_sock.host.wait_for_message()
    recv_sock.stop()
    recv_sock.join()
    