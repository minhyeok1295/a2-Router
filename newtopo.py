# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 22:41:07 2022

@author: MinHyeok
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

class SingleSwitchTopo(Topo):
    
    def __init__(self, n=2, **opts):
        Topo.__init__(self, **opts)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        r1 = self.addNode('r1')
        #Add Links
        self.addLink(h1,s1)
        self.addLink(h2,s1)
        self.addLink(h3,s2)
        self.addLink(h4,s2)
        self.addLink(s2,r1)
        self.addLink(s1,r1)
        

if __name__ == "__main__":
    setLogLevel('info')
    
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    net.stop()
