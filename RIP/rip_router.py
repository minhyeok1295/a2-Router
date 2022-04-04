
from router import *
from rip_table import RIPTable
import time
import ifaddr
from interface import Interface 

class RIPRouter(Router):

    def __init__(self):
        self.table = RIPTable()
        self.init_update_sock()
        self.interfaces = self.init_interfaces()
        self.interface_ip = [interface.ip for interface in self.interfaces]
        self.interface_lock = self.init_locks()
        self.table_lock = threading.Lock()
        self.init_table()
        self.update_table_timer = []
        self.advertise_table_timer = []
    
    def start(self):
        broadcast_t = ThreadSock(self)
        update_t = UpdateThread(self)
        threads = [broadcast_t,update_t]
        broadcast_t.start()
        update_t.start()
        recv_threads = []
        for interface in self.interfaces:
            recv_thread = ReceiveThread(self,interface)
            recv_thread.start()
            threads.append(recv_thread)
        time.sleep(1)
        # broadcast message to all interfaces in the list
        self.advertise()
        self.start_command()
        for thread in threads:
            thread.stop()
        for thread in threads:
            thread.join()

    # stores all the interface this router connects to in the interfaces
    def init_interfaces(self):
        interfaces = []
        adapters = ifaddr.get_adapters()
        for adapter in adapters:
            name = adapter.name.split("-")
            if name[-1][:3] == "eth":
                ips = adapter.ips[0]
                interfaces.append(Interface(ip=ips.ip,prefix=ips.network_prefix))
        return interfaces

    # initialize one thread lock for every interface
    # used to sending messages
    def init_locks(self):
        return [threading.Lock() for i in self.interfaces]

    # add interfaces to table
    def init_table(self):
        print("=========== Initializing Table ===========")
        for interface in self.interfaces:
            self.table.set_entry(interface.ip,[interface.ip,interface.interface,0])
        print(self.table)
        print("=========== Done Initializing Table ===========")

    # overwrite original receive for broadcasr channel
    def receive(self): #wait for broadcast
        recv_data, addr = self.thread_sock.recvfrom(1024)
        data = pickle.loads(recv_data)
        self.table_lock.acquire()
        # set src ip as key, the ip where the message is coming from as value
        cur_interface = None
        for interface in self.interfaces:
            if interface.calc_interface(data['src_ip'],interface.prefix) == interface.interface:
                self.table.set_entry(data['src_ip'],[addr[0],interface.interface,1])
                cur_interface = interface
                break
        self.table_lock.release()
        self.thread_sock.sendto(make_packet(interface.ip,addr,'',0),addr)
        self.advertise()
    
    def init_advertise_sock(self,ip):
        self.advertise_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.advertise_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.advertise_sock.bind((ip,ADVERTISE_PORT))

    def init_update_sock(self):
        self.update_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.update_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.update_sock.bind(('0.0.0.0',UPDATE_PORT))

    # this is in requirement, but not sure why we need this.
    def set_forwarding_table(self,table):
        if (self.is_valid_table(table)):
            self.table.set_table(table)
        else:
            print("got an invalid table for RIP")
    
    def is_valid_table(self,table):
        for k,v in table.items():
            if not validate_ip(k):
                return False
            if len(v) != 3:
                return False
            if not validate_ip(v[0]):
                return False
        return True
    
    def advertise(self):
        print("======== Advertising ========")
        self.table_lock.acquire()
        start_time = time.time()
        for interface in self.interfaces:
            self.init_advertise_sock(interface.ip)
            data = make_table(self.table.get_table())
            self.advertise_sock.sendto(data,('255.255.255.255', UPDATE_PORT))
            self.advertise_sock.close()
        self.advertise_table_timer.append(time.time()-start_time)
        self.table_lock.release()
        print("======== Done Advertising ========")

    def update(self,table,last_hop,interface):
        print("======== Got Update Message ========")
        table = table.copy()
        start_time = time.time()
        if len(self.table.get_table().keys()) == 0:
            self.set_forwarding_table(table)
            return
        modified = False
        self.table_lock.acquire()
        prev_table = self.table.get_table()
        for k,v in table.items():
            val = int(v[2])
            if k in prev_table:
                if val < prev_table[k][2] - 1:
                    self.table.set_entry(k,[last_hop,interface.interface,val+1])
                    modified = True
            else:
                self.table.set_entry(k,[last_hop,interface.interface,val+1])
                modified = True
        print(self.table)
        self.table_lock.release()
        self.update_table_timer.append(time.time()-start_time)
        print("======== Done Update Message ========")
        if modified:
            self.advertise()
    
    def init_forward_sock(self,interface):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((interface.ip,RECV_PORT))
        server.listen(5)
        return server

    def forward(self,sock):
        conn, addr = sock.accept()
        print("Server connected to", addr)
        packet = conn.recv(4096)
        conn.close()
        if len(packet) != 0:
            data = pickle.loads(packet)
            print_packet(data)
            data['ttl'] -= 1
            if (data['ttl'] > 0):
                dest = data['dest_ip']
                self.table_lock.acquire()
                if self.table.has_ip(dest):
                    table_entry = self.table.get_next_hop(dest)
                    self.send(data,table_entry)
                else:
                    print_error(data['src_ip'],data['dest_ip'])
                self.table_lock.release()
            else:
                print("========== TTL Expired ==========")
                print(f"TTL expired from {data['src_ip']} to {data['dest_ip']}\n\n")
        else:
            print("nothing received")
    
    def send(self,data,table_entry):
        packet = make_packet(data['src_ip'],data['dest_ip'],data['message'],data['ttl'])
        for i in range(len(self.interfaces)):
            self.interface_lock[i].acquire()
            if self.interfaces[i].interface == table_entry[1]:
                send_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                send_sock.bind((self.interfaces[i].ip,SEND_PORT))
                send_sock.connect((table_entry[0],RECV_PORT))
                send_sock.send(packet)
                send_sock.close()
                print("socket is closed")
                self.interface_lock[i].release()
                break
            self.interface_lock[i].release()
    
    def start_command(self):
        print("Start Command")
        command = ''
        while command != 'exit':
            command = input()
            print("Command you entered is ",command)
            if command == "print":
                print("Executing print command")
                print(self.table)
            if command == "print2":
                self.table.print2()
            if command == "timer":
                print("Printing Time Measurement")
                print("Time Spent on Updating Table")
                print(self.update_table_timer)
                print("Sum : ", sum(self.update_table_timer))
                if len(self.update_table_timer) > 0:
                    print("Average : ",sum(self.update_table_timer)/len(self.update_table_timer))
                print("Time Spent on Advertising Table")
                print(self.advertise_table_timer)
                print("Sum : ", sum(self.advertise_table_timer))
                if len(self.advertise_table_timer) > 0:
                    print("Average : ",sum(self.advertise_table_timer)/len(self.advertise_table_timer))



class UpdateThread(ThreadSock):
    
    def run(self):
        while not self.stopped():
            recv_data,addr = self.node.update_sock.recvfrom(4096)
            for interface in self.node.interfaces:
                if interface.calc_interface(addr[0],interface.prefix) == interface.interface:
                    if addr[0] != interface.ip:
                        data = pickle.loads(recv_data)
                        if "table" in data.keys():
                            self.node.update(data['table'],addr[0],interface)
                        else:
                            print(f"Got invalid table message from {addr}")
                    break
        self.node.update_sock.close()

class ReceiveThread(ThreadSock):
    """
    For each interface, we initialize an socket for forwarding messages
    """

    def __init__(self,router:RIPRouter,interface:Interface):
        super().__init__(router)
        # initialize a socket based on the interface
        self.recv_socket = self.node.init_forward_sock(interface)
    
    def run(self):
        while not self.stopped():
            self.node.forward(self.recv_socket)
        self.recv_socket.close()

if __name__ == "__main__":
    router = RIPRouter()
    router.start()

