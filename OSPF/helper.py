import pickle
import threading

SEND_PORT = 8000
RECV_PORT = 8100
BRAODCAST_ADDR = '255.255.255.255'
BRAODCAST_PORT = 9999
UPDATE_PORT = 8200
ADVERTISE_PORT = 8300


class ThreadSock(threading.Thread):
    
    def __init__(self,node):
        threading.Thread.__init__(self)
        self.node = node
        # https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        self.node.open_thread_sock()
        while not self.stopped():
            self.node.receive()
        self.node.thread_sock.close()


class TableCommandThread(ThreadSock):
    def run(self):
        print("Start Command Thread")
        while not self.stopped():
            command = input()
            if command == "print":
                print(self.node.table)
            if command == "connect":
                ip = input("Enter Ip address: ")
                self.node.notify_monitor_connect(ip)
            if command == "disconnect":
                self.node.notify_monitor_disconnect()
            if command == "time"
                print(self.node.total_time / self.num)

#Make message packet and dump it into pickle
def make_packet(src_ip, dest_ip, message, ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dumps(data)

#save table inforamtion for RIP algorithm
def make_table(table):
    return pickle.dumps({
        "table": table
    })

#include table information and the corresponding routers for sending purpose.
def make_table_packet(src_ip, dest_ip, table, neighbors):
    data = {
        'src_ip': src_ip,
        'dest_ip': dest_ip,
        'table': table,
        'neighbors': neighbors,
        'packet' : "table"
    }
    return pickle.dumps(data)


def print_packet(packet):
    print("-----packet info-----")
    print("src_ip: " + packet["src_ip"])
    print("dest_ip: " + packet["dest_ip"])
    print("msg: " + packet['message'])
    print("ttl: " + str(packet['ttl']))
    print("=====================")
    
def print_error(src_ip,dest_ip):
    print("========== Error ==========")
    print(f"Bad request from {src_ip}")
    print(f"Destination {dest_ip} is unreachable\n\n")

def print_ttl_expired(cur_ip, data):
    print("========== TTL Expired ==========")
    print_packet(data)
    print(f"Package dropped At router {cur_ip} from {data['src_ip']} to {data['dest_ip']}\n\n")

#Validate format of ip address
def validate_ip(ip):
    nums = ip.split(".")
    if len(nums) != 4:
        return False
    for i in range(len(nums)):
        try:
            num = int(nums[i])
        except:
            return False
        if (num > 255 or num < 0):
            return False
    return True


def check_on_same_switch(ip1, ip2):
    if(ip1.split(".")[:3] == ip2.split(".")[:3]):
        return True
    return False