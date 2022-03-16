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


class Router():
    
    def __init__(self, ip):
        self.ip = ip
        self.bc_sock = None

    def init_bc_sock(self):
        self.bc_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.bc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.bc_sock.bind(('0.0.0.0',9999))

    def wait_for_broadcast(self):
        recv_data, addr = self.bc_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.bc_sock.sendto(make_packet(self.ip,addr,'',0),addr)
    
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
            if not self.forward(data):
                self.print_error(data['src_ip'],data['dest_ip'])
            else:
                print(f"Successfully sent message to {data['dest_ip']}")
            conn.close()
        conn.close()
        server.close()

    def forward(self,recv_data):
        data =recv_data.copy()
        packet = make_packet(data['src_ip'],data['dest_ip'],data['message'],data['ttl'])
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try : 
            print("connect")
            sock.connect((data['dest_ip'],8100))
            print("send")
            sock.send(packet)
            print("close")
            sock.close()
        except Exception:
            sock.close()
            return False
        return True
    
    def print_error(self,src_ip,dest_ip):
        print("========== Error ==========")
        print(f"Bad request from {src_ip}")
        print(f"Destination {dest_ip} is unreachable\n\n")


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

      
class ServerThread(threading.Thread):
    """ We don't need this yet
    """
    
    def __init__(self,router):
        threading.Thread.__init__(self)
        self.router = router
    
    def run(self):
        self.router.open_server()




if __name__ == "__main__":
    router = Router("10.0.0.1")
    broadcast_t = BroadCastThread(router)
    broadcast_t.start()
    router.open_server()
    broadcast_t.stop()
    router.bc_sock.close()
    broadcast_t.join()
    #1. receive broadcast message
    #2. send packet to host who sent broadcast message
    #3. forward the message packet received to the final destination
    