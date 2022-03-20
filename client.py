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
client.connect(('127.0.0.1', 8080))

print("here")
x = input("Enter name: ")
print("Hello, " + x)
print("here2")
client.send("here3")
from_server = client.recv(4096)
client.close()
print(from_server)