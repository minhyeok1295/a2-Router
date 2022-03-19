import sys
import socket

#cmd line arg: python3 host.py ip

s = socket.socket()
host = socket.gethostname()
print(host)
port = 8000



s.connect((host, port))
print(s.recv(1024))
s.close()


if __name__ == "__main__":
    arg = sys.argv
    ip = sys.argv[1]
    ttl = sys.argv[2]
    print("ip: ", ip, " ttl: ", ttl)
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.bind((ip, 8000))