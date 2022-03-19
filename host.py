import sys
import socket

#cmd line arg: python3 host.py ip

def main(argv)
    ip = argv[1]
    connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connection.bind((ip,8000)) # host port 8000
    





if __name__ == "__main__":
    main(sys.argv)
    
    
