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
#/usr/bin.python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
'''
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
'''

class SingleSwitchTopo(Topo):
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        switch = self.addSwitch('s1')

        for h in range(n):
            host = self.addHost('h%s'%(h+1))
            self.addLink(host, switch)


def simpleTest():
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    print("dumping host connections")
    dumpNodeConnections(net.hosts)
    print("testing network connectivity")
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()

