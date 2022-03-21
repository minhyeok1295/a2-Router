import socket
import pickle
from helper import *

broadcast = '255.255.255.255'
inter1= '172.168.0.1'
inter2= '192.168.1.1'


class Router():
    
    def __init__(self, ip):
        self.ip = ip
    
    def wait_for_broadcast(self):
        bc_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        bc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        bc_sock.bind(('0.0.0.0',9999))
        while True:
            recv_data, addr = bc_sock.recvfrom(1024)
            data = pickle.loads(recv_data)
            print(data['src_ip'])
            print(addr)
            bc_sock.sendto(make_packet(self.ip,addr,'',0),addr)
            break
        bc_sock.close()
    
    def open_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            pacekt = conn.recv(4096)
            data = pickle.loads(packet)
            print(data['message'])
            msg = "server received message: " + data['message']
            conn.send(msg.encode())
            conn.close()
            
            

        






if __name__ == "__main__":
    router = Router("10.0.0.1")
    while True:
        router.wait_for_broadcast()
        #receive message
        router.open_server()

    """
    src_name = socket.gethostname()
    src_ip = "10.0.0.2"

    bc_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    bc_sock.bind((broadcast,8000))
    bc_sock.listen(5)

    router_in = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    router_in.bind((src_ip,8100)) # router recieve port 8100
    router_in.listen(5)

    router_out = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    router_out.bind((src_ip,8200)) # router send port 8200
    router_out.listen(5)

    while True:
        hostsocket, addr = router_in.accept()
        print("host addr ",addr)
        data = hostsocket.recv(1024)
        if data:
            if data['dest_ip'] == broadcast:
                hostsocket.send(make_packet(src_ip,addr,'',0))
        hostsocket.close()
    """
    #1. receive broadcast message
    #2. send packet to host who sent broadcast message
    #3. forward the message packet received to the final destination
    