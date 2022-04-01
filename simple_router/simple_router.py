from router import *
from helper import *
from ospf_table import *

class SimpleRouter(Router):
    def __init__(self, ip):
        super().__init__(ip)
        self.table = SimpleTable()
        
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        if (check_on_same_switch(self.ip, data['src_ip'])):
            self.lock.acquire()
            # set src ip as key, the ip where the message is coming from as value 
            self.table.create_entry( data['src_ip'], addr[0])
            self.table.add_neighbors(data['src_ip'], "host")
            self.lock.release()
            self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
        else: #it is router
            self.thread_sock.sendto(make_packet(self.ip,addr,'NA',0),addr)
    
    def send_attach(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 8000))
        s.send(make_packet(self.ip, ip, "cr", -1))
        s.close()
        self.lock.acquire()
        dip = ip.rpartition(".")[0]
        self.table.create_entry(dip, ip)
        self.table.add_neighbors(ip, "router")
        self.lock.release()
        
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
                if (data['message'] == 'cr' and data['ttl'] == -1): #connecting router
                    
                    self.lock.acquire()
                    # set src ip as key, the ip where the message is coming from as value 
                    dip = data['src_ip'].rpartition(".")[0]
                    self.table.create_entry(dip + ".0", data['src_ip'])
                    self.table.add_neighbors(data['src_ip'], "router")
                    self.lock.release()
                
                elif (data['message'] == 'exit'):
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