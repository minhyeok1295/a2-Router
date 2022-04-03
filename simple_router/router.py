import socket
import pickle
import threading
from helper import *
import sys
broadcast = '255.255.255.255'


class Router():
    
    def __init__(self, ip):
        self.ip = ip
        self.thread_sock = None
        self.lock = threading.Lock()

    def open_thread_sock(self):
        self.thread_sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.thread_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.thread_sock.bind(('255.255.255.255',9999))

