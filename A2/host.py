import socket
import pickle
import sys

broadcast = '255.255.255.255'
def make_packet(src_ip,dest_ip,message,ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dumps(data)

if __name__ == "__main__":
    address = (sys.argv[1], 9999)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    while True:
        print(broadcast)
        s.sendto(make_packet(address,broadcast,'',0),(broadcast,9999))
        recv_data, addr = s.recvfrom(1024)
        data = pickle.loads(recv_data)
        print(data['src_ip'])
        break
    s.close()
    """connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.bind((src_ip,8000)) # host port 8000
    connection.connect(("10.0.0.2",8100))   # router broadcast port 8000
    connection.send(make_packet(src_ip,broadcast,'',0))
    recv_data = connection.recv(1024)
    connection.close()
    data = pickle.load(recv_data)
    router_ip = data['src_ip']
    print(router_ip)"""
    

