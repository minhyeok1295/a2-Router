'''
import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 8000))
    msg = s.recv(1024)
    print(msg.decode("utf-8"))
    
'''
import sys
import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('10.0.0.1', 8000))

print("here")
x = sys.stdin.readline()
msg = "My name is " + x
client.send(msg)
from_server = client.recv(4096)
client.close()
print(from_server)