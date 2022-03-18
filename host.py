import socket
'''
#Simple end system with a signle IP address
class EndSystem:
    def __init__(self, ip, nxt):
        self.ip = ip
        self.nxt = nxt
        
    def send(self, dest_ip, message, ttl):
        pass
    
    def receive(self, source_ip):
        pass
'''
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

net = Mininet()

c0 = net.addController()
h0 = net.addHost('h0')
s0 = net.addSwitch('s0')
h1 = net.addHost('h1')

net.addLink(h0, s0)
net.addLink(h1, s0)

h0.setIP('192.168.1.1', 24)
h1.setIP('192.168.1.2', 24)

net.start
net.pingAll()
net.stop()
