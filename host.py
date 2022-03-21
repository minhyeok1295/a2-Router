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
            if(msg[:-1] == 'exit'):
                break
            print("Enter destination: ")
            dest_ip = input("Enter input destination: ")
            print("msg is ", msg)
            print("dest is ", dest_ip)
            self.connect()
            data_packet = make_packet(self.ip, dest_ip, msg, 2)
            self.send_sock.send(data_packet)
            self.send_sock.close()

    def init_recv_sock(self):
        self.recv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.recv_sock.bind((self.ip, 8100))
        self.recv_sock.listen(5)
    '''
    if an end system receives a message, it should display that message
    (and any other relevant information) to its output
    '''
    def receive(self):
        recv_sock,addr = self.recv_sock.accept()
        recv_data = self.recv_sock.recv(4096)
        data = data.pickle.loads(recv_data)
        print(data)
        print(f"From {data['src_ip']}: {data['message']}")
        recv_sock.close()
        

class ReceiveThread(threading.Thread):
    
    def __init__(self,host):
        threading.Thread.__init__(self)
        self.host=host
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.host.init_recv_sock()
        while not self.stopped():
            self.host.receive()
        self.host.recv_sock.close()



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

    recv_t = ReceiveThread(host)
    recv_t.start()
    host.send()
    recv_t.stop()
    recv_t.join()
    print('Program Terminated')
    