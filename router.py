import socket
import pickle
import threading
from helper import *
from _thread import start_new_thread

broadcast = '255.255.255.255'
inter1= '172.168.0.1'
inter2= '192.168.1.1'

def print_packet(packet):
    print("-----packet info-----")
    print("src_ip: " + packet["src_ip"])
    print("dest_ip: " + packet["dest_ip"])
    print("msg: " + packet['message'])
    print("ttl: " + str(packet['ttl']))


def multi_thread_client(conn, clients):
    print(clients)
    while True:
        packet = conn.recv(4096)
        try:
            data = pickle.loads(packet)
            if (data['dest_ip'] not in clients):
                print("destination is not reachable")
                conn.send(str.encode("destination is not reachable"))
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((data['dest_ip'], 8100))
            print("connected to " + data['dest_ip'])
            clients[data['dest_ip']] = sock
            sock.send(packet)
            sock.close()
            print_packet(data)
            
            print("======sent=====")
            
            msg = "sent msg to: " + data['dest_ip']
            if (data['message'] == 'exit'):
                conn.send(msg.encode())
                break
            conn.sendall(msg.encode())
        except EOFError:
            pass


class Router():
    
    def __init__(self, ip):
        self.ip = ip
        self.bc_sock = None
        self.clients = {}
        

    def init_bc_sock(self):
        self.bc_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.bc_sock.bind(('0.0.0.0',9999))

    def wait_for_broadcast(self):
        recv_data, addr = self.bc_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.clients[data['src_ip']] = None
        print(addr)
        self.bc_sock.sendto(make_packet(self.ip,self.ip,'',0),addr)
    
    def open_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        print("listening...")
        while True:
            conn, addr = server.accept()
            print("-----Connected------")
            print(addr)
            start_new_thread(multi_thread_client, (conn, self.clients))
          
class BroadCastThread(threading.Thread):
    
    def __init__(self,router):
        threading.Thread.__init__(self)
        self.router = router
        # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.router.init_bc_sock()
        while not self.stopped():
            self.router.wait_for_broadcast()
        self.router.bc_sock.close()



if __name__ == "__main__":
    router = Router("10.0.0.1")

    broadcast_t = BroadCastThread(router)
    broadcast_t.start()
    router.open_server()
    broadcast_t.stop()
    broadcast_t.join()
    #1. receive broadcast message
    #2. send packet to host who sent broadcast message
    #3. forward the message packet received to the final destination
    