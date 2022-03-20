import socket
import sys


class Host():
    '''
    given the end system's IP addr ess, the end system will become active, open socke to its next hop connection
    and send a simple message to the IP address 255.255.255.255 with TTL=0 in order to broadcast its existence
    '''
    
    def __init__(self, ip, next_ip):
        self.ip = ip
        self.ttl = 0
        self.next_ip = next_ip
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.next_ip, 8000))
        
        
    '''Given a destination IP address, a text message and TTL,
    the end system will attempt to send the message through the network
    '''
    def send(self, dest_ip, message, ttl):
        pass
    
    '''
    if an end system receives a message, it should display that message
    (and any other relevant information) to its output
    '''
    def receive(self):
        pass



if __name__ == "__main__":
    #ip = sys.argv[1]
    next_ip = sys.argv[1]
    print("next: " + next_ip)
    #ttl = sys.argv[3]
    
   # h = Host(ip, next_ip)
    host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host.connect((next_ip, 8000))
   # host = h.socket
    msg = sys.stdin.readline()
    host.send(msg)
    from_server = host.recv(4096)
    host.close()
    
    print(from_server)
    
    
    