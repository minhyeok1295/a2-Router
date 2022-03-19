import socket

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8000
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    
    while True:
        c, addr = server.acecpt()
        print("connection established")
        
        string = c.recv(1024)
        string = string.decode("utf-8")
        print(string)