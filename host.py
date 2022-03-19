import socket

if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8000
    
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)