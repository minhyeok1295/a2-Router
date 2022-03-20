# -*- coding: utf-8 -*-
import socket
import sys

if __name__ == "__main__":
    ip = sys.argv[1]    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, 8000))
    s.listen(5)
    print("listening....")
    while True:
        conn, addr = s.accept()
        from_client = ""
        while True:
            data = conn.recv(4096)
            if not data:
                break
            from_client += data
            print("from_client: " + from_client)
            conn.send("message has been received")
        conn.close()
        break