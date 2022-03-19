import socket
import pickle

broadcast = '255.255.255.255'
interface_ip = '127.0.0.'
def make_packet(src_ip,dest_ip,message,ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dumps(data)

if __name__ == "__main__":
    print("Please Enter an IP address")
    src_ip = interface_ip + input()
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.bind((src_ip,8000)) # host port 8000
    connection.connect((broadcast,8000))   # router broadcast port 8000
    connection.send(make_packet(src_ip,broadcast,'',0))
    recv_data = connection.recv(1024)
    connection.close()
    data = pickle.load(recv_data)
    router_ip = data['src_ip']
    print(router_ip)
    

