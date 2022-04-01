from router import *

class OSPFRouter(Router):
    def __init__(ip):
        super.__init__(ip)
        
    def notify_monitor_new_router(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.1", 8888))
        s.send(make_packet(self.ip, "10.0.0.1", "router", 0))
        s.close()
        
    def notify_monitor_new_host(self, ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("10.0.0.1", 8888))
        s.send(make_packet(ip, self.ip, "host", 0))
        s.close()
    
    def open_server(self):
        self.notify_monitor_new_router()
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.ip, 8000))
        server.listen(5)
        while True:
            conn, addr = server.accept()
            print("Server connected to")
            print(addr)
            self.notify_monitor_new_host()
            packet = conn.recv(4096)
            if len(packet) != 0:
                data = pickle.loads(packet)
                print_packet(data)
                if (data['message'] == 'exit'):
                    break
                data['ttl'] -= 1
                if (data['ttl'] > 0):
                    dest = data['dest_ip']
                    self.lock.acquire()
                    if self.table.has_ip(dest):
                        next_hop = self.table.get_next_hop(dest)
                        print(next_hop)
                        try:
                            self.forward(data,next_hop)
                            print(f"Successfully sent message to {data['dest_ip']}")
                        except Exception:
                            print("Error!!!!")
                    else:
                        print_error(data['src_ip'],data['dest_ip'])
                    self.lock.release()
                else:
                    print_ttl_expired(self.ip,data['src_ip'],data['dest_ip'])
            else:
                print("nothing received")
            conn.close()
        conn.close()
        server.close()
        
    
        

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("error occured")
        exit(1)
    router = OSPFRouter(sys.argv[1])
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