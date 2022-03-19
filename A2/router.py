import socket
import pickle

broadcast = '255.255.255.255'

def make_packet(src_ip,dest_ip,message,ttl):
    data = {
        'src_ip' : src_ip,
        'dest_ip' : dest_ip,
        'message' : message,
        'ttl' : ttl
    }
    return pickle.dump(data)

if __name__ == "__main__":
    src_name = socket.gethostname()
    src_ip = "127.0.0.200"

    bc_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    bc_sock.bind((broadcast,8000))
    bc_sock.listen(5)

    router_in = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    router_in.bind((src_ip,8100)) # router recieve port 8100
    router_in.listen(5)

    router_out = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    router_out.bind((src_ip,8200)) # router send port 8200
    router_out.listen(5)

    while True:
        hostsocket, addr = bc_sock.accept()
        print("host addr ",addr)
        data = hostsocket.recv(1024)
        if data:
            if data['dest_ip'] == broadcast:
                hostsocket.send(make_packet(src_ip,addr,'',0))
        hostsocket.close()
    

    