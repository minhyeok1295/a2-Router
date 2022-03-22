import socket
import pickle
import sys
from helper import ThreadSock, make_packet

import threading



def print_packet(packet):
    print("-----packet info-----")
    print("src_ip: " + packet["src_ip"])
    print("dest_ip: " + packet["dest_ip"])
    print("msg: " + packet['message'])
    print("ttl: " + str(packet['ttl']))

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
        self.thread_sock = None
    
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
            
    def open_socket(self, router_ip):
        
        while True:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((router_ip, 8000))
            print("=============================")
            msg = input("Enter Message: ")
            dest = input("Enter destination IP: ")
            ttl = input("Enter ttl: ")
            if (ttl != "0"):
                print("send to " + dest + ",msg: " + msg + ", ttl: " + ttl)
                data_packet = make_packet(self.ip, dest, msg, int(ttl))
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

    def open_thread_sock(self):
        self.thread_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread_sock.bind((self.ip, 8100))
        self.thread_sock.listen(5)
    
        
    '''
    if an end system receives a message, it should display that message
    (and any other relevant information) to its output
    '''
    def receive(self):
        
        while True:
            c, a = self.thread_sock.accept()
            print("\n")
            packet = c.recv(4096)
            data = pickle.loads(packet)
            print("from: " + data['src_ip'] + ", msg: " + data['message'])
            print("Enter Message: ")

class RecvSockThread(threading.Thread):
    
    def __init__(self,host):
        threading.Thread.__init__(self)
        self.host = host
        # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        self._stop_event = threading.Event()
        
        #self.host.open_recv_sock()
    
    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        
        self.host.open_recv_sock()
        while not self.stopped():
            self.host.receive()
        self.host.close_recv_sock()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Incorrect number of arguments: IP address needed")
        raise
    host = Host(sys.argv[1], 9999)
    print("created host")
    recv_sock = ThreadSock(host)
    print("Start broadcasting")
    data = host.broadcast()
    
    recv_sock.start()
    host.open_socket(data['src_ip']) #router_ip
    recv_sock.stop()
    recv_sock.join()
    