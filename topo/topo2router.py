# -*- coding: utf-8 -*-

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.node import RemoteController

topos = { 'mytopo': ( lambda: NetworkTopo() ) } 

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 2 routers in two different subnets1
        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        sm = self.addSwitch('s3')

        # Add host-switch links in the same subnet
        self.addLink(sm, m, intfName2='m-eth0', params2={'ip': '10.0.0.1/24'})
    
        self.addLink(s1, r1, intfName2='r1-eth0', params2={'ip': '10.1.0.1/24'})

        self.addLink(s2, r2, intfName2='r2-eth0', params2={'ip': '10.2.0.1/24'})
        
        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1, r2, intfName1='r1-eth1', intfName2='r2-eth1', params1={'ip': '10.10.0.1/24'}, params2={'ip': '10.10.0.2/24'})
        
        self.addLink(r1, m, intfName1='r1-eth2', intfName2='m-eth1', params1={'ip': '10.101.0.1/24'}, params2={'ip': '10.101.0.2/24'})
        self.addLink(r2, m, intfName1='r2-eth2', intfName2='m-eth2', params1={'ip': '10.102.0.1/24'}, params2={'ip': '10.102.0.2/24'})
        
        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1',ip='10.1.0.10/24',defaultRoute='via 10.1.0.1')
        
        #h2 = self.addHost(name='h2', ip='10.0.0.20/24', defaultRoute='via 10.0.0.1')
        
        h3 = self.addHost(name='h3', ip='10.2.0.10/24', defaultRoute='via 10.2.0.1')
        
        #h4 = self.addHost(name='h4', ip='10.1.0.20/24', defaultRoute='via 10.1.0.1')
        '''
        h5 = self.addHost(name='h5',
                          ip='10.2.0.10/24',
                          defaultRoute='via 10.2.0.1')
        
        
        h6 = self.addHost(name='h6',
                          ip='10.2.0.20/24',
                          defaultRoute='via 10.2.0.1')
        '''
        # Add host-switch links
        self.addLink(h1, s1)
        #self.addLink(h2, s1)
        
        self.addLink(h3, s2)
        #elf.addLink(h4, s2)
        
        #self.addLink(h5, s3)
        #self.addLink(h6, s3)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()

    # Add routing for reaching networks that aren't directly connected
    

    # type the following command in the mininet shell
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.10.0.2 dev r1-eth1"))
    
    info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.101.0.2 dev r1-eth2"))
    
    info(net['r2'].cmd("ip route add 10.1.0.0/24 via 10.10.0.1 dev r2-eth1"))
    
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.102.0.2 dev r2-eth2"))
    
    info(net['m'].cmd("ip route add 10.1.0.0/24 via 10.101.0.1 dev m-eth1"))
    info(net['m'].cmd("ip route add 10.2.0.0/24 via 10.102.0.1 dev m-eth2"))
    
    net.startTerms()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()