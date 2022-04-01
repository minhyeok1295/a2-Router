from router import *
from helper import *
from simple_table import *

class SimpleRouter(Router):
    def __init__(self, ip):
        super().__init__(ip)
        self.table = SimpleTable()
        
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.lock.acquire()
        # set src ip as key, the ip where the message is coming from as value 
        self.table.create_entry( data['src_ip'], addr[0])
        self.table.add_neighbors(data['src_ip'], "host")
        self.lock.release()
        self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
    
    def open_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Server connected")
            packet = conn.recv(4096)
            if len(packet) != 0:
                data = pickle.loads(packet)
                if (data['message'] == 'exit'):
                    break
                else:
                    data['ttl'] -= 1
                    if (data['ttl'] > 0):
                        dest = data['dest_ip']
                        self.lock.acquire()
                        next_hop, t = self.table.check_ip(dest)
                        if next_hop != None:
                            try:
                                self.forward(data,next_hop, t)
                                print(f"Successfully sent message to {t}, {next_hop}")
                            except Exception:
                                print("Error!!!!")
                        else:
                            print_error(data['src_ip'],data['dest_ip'])
                        self.lock.release()
                    else:
                        print_ttl_expired(self.ip,data)
            else:
                print("nothing received")
            conn.close()
        conn.close()
        server.close()
        
    
        

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    router = SimpleRouter(sys.argv[1])
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