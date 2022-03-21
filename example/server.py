'''
import socket

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8000
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.listen(5)
    
    while True:
        c, addr = server.accept()
        print("connection established")
        
        c.send(bytes("welcome to the server!", "utf-8"))
        
'''
import socket
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('127.0.0.200', 9999))
serv.listen(5)
while True:
    conn, addr = serv.accept()
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data
        print(from_client)
        conn.send("I am SERVER")
    conn.close()
    print('client disconnected')
    break