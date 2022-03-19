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
