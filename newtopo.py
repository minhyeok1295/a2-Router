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
        switch = self.addSwitch("s1")
        
        
        for h in range(n):
            host = self.addHost('h%s'%(h+1))
            self.addLink(host, switch)
            

if __name__ == "__main__":
    setLogLevel('info')
    
    topo = SingleSwitchTopo(n=4)
    net = Mininet(topo)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    net.stop()
