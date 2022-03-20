# -*- coding: utf-8 -*-
"""
Created on Sun Mar 20 18:35:12 2022

@author: MinHyeok
"""
import socket

if __name__ == "__main__":
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    
    print(local_ip)
    print(hostname)