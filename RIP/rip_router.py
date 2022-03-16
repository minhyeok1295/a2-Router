from router import *
from rip_table import RIPTbable
import time
class RIPRouter(Router):

    def __init__(self,ip):
        super().__init__(ip)
        self.table = RIPTbable(ip)
        self.init_update_sock()
    
    # overwrite orgiginal receive for broadcasr channel
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.lock.acquire()
        # set src ip as key, the ip where the message is coming from as value
        self.table.set_entry(data['src_ip'],[addr[0],1])
        self.lock.release()
        self.thread_sock.sendto(make_packet(self.ip,addr,'',0),addr)
    
    def init_advertise_sock(self):
        self.advertise_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.advertise_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.advertise_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def init_update_sock(self):
        self.update_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.update_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.update_sock.bind(('0.0.0.0',8200))

    # this is in requirement, but not sure why we need this.
    def set_forwarding_table(self,table):
        if (self.is_valid_table(table)):
            print("Check valid table")
            print(table)
            self.table.set_table(table)
            print(self.table.get_table())
        else:
            print("got an invalid table for RIP")
    
    def is_valid_table(self,table):
        for k,v in table.items():
            if not validate_ip(k):
                return False
            if len(v) != 2:
                return False
            if not validate_ip(v[0]):
                return False
        return True
    
    def advertise(self):
        self.init_advertise_sock()
        print("======== Loading Table ========")
        self.lock.acquire()
        data = make_table(self.table.get_table())
        self.lock.release()
        print("======== Advertising Table ========")
        self.advertise_sock.sendto(data,('255.255.255.255', 8200))
        self.advertise_sock.close()

    def update(self,table,last_hop):
        print("======== Got Update Message ========")
        table[last_hop] = [table[last_hop][0],1]
        if len(self.table.get_table().keys()) == 0:
            self.set_forwarding_table(table)
            return
        modified = False
        self.lock.acquire()
        prev_table = self.table.get_table()
        for k,v in table.items():
            val = int(v[1])
            if k in prev_table:
                if val > 0 and val < prev_table[k][1]:
                    self.table.set_entry(k,[v[0],val])
                    modified = True
            else:
                self.table.set_entry(k,[v[0],val])
                modified = True
        print(self.table)
        self.lock.release()
        if modified:
            self.advertise()
        
        

class TableCommandThread(ThreadSock):
    def run(self):
        print("Start Command Thread")
        while not self.stopped():
            command = input()
            print("Command you entered is ",command)
            if command == "print":
                print("Executing print command")
                print(self.node.table)
            if command == "print2":
                self.node.table.print2()
        

class UpdateThread(ThreadSock):
    
    def run(self):
        while not self.stopped():
            recv_data,addr = self.node.update_sock.recvfrom(4096)
            data = pickle.loads(recv_data)
            if "table" in data.keys():
                self.node.update(data['table'],addr[0])
            else:
                print(f"Got invalid table message from {addr}")
        self.node.update_sock.close()

if __name__ == "__main__":
    ip = input("please enter the router ip: ")
    router = RIPRouter(ip)
    broadcast_t = ThreadSock(router)
    command_t = TableCommandThread(router)
    update_t = UpdateThread(router)
    broadcast_t.start()
    command_t.start()
    update_t.start()
    try:
        time.sleep(1)
        router.advertise()
    except Exception:
        pass
    router.open_server()
    broadcast_t.stop()
    command_t.stop()
    update_t.stop()
    router.thread_sock.close()
    broadcast_t.join()
    command_t.join()
    update_t.stop()
