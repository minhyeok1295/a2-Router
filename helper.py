import pickle
import threading


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



def make_packet(src_ip, dest_ip, message, ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dumps(data)



def print_packet(packet):
    print("-----packet info-----")
    print("src_ip: " + packet["src_ip"])
    print("dest_ip: " + packet["dest_ip"])
    print("msg: " + packet['message'])
    print("ttl: " + str(packet['ttl']))
    
    
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