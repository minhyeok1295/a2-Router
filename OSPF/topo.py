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
        # Add 2 routers in two different subnets
        m = self.addHost('m', cls=LinuxRouter, ip='10.0.0.1/24' )
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.1.0.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.2.0.1/24')
        #r3 = self.addHost('r3', cls=LinuxRouter, ip='10.3.0.1/24')
        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        #s3 = self.addSwitch('s3')

        # Add host-switch links in the same subnet
        self.addLink(s1, r1, intfName2='r1-eth0', params2={'ip': '10.1.0.1/24'})
        self.addLink(s2, r2, intfName2='r2-eth0', params2={'ip': '10.2.0.1/24'})
        #self.addLink(s3, r3, intfName2='r3-eth0', params2={'ip': '10.3.0.1/24'})

        #add router-monitor link
        self.addLink(m, r1, intfName1='m-eth1', intfName2='r1-eth1', params1={'ip': '10.11.0.1/24'}, params2={'ip': '10.11.0.2/24'}) 
        self.addLink(m, r2, intfName1='m-eth2', intfName2='r2-eth1', params1={'ip': '10.12.0.1/24'}, params2={'ip': '10.12.0.2/24'})       
        #self.addLink(m, r3, intfName1='m-eth1', intfName2='r3-eth1', params1={'p': '10.12.0.1/24'}, params2={'ip': '10.12.0.2/24'})        
        
        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip': '10.100.0.1/24'}, params2={'ip': '10.100.0.2/24'})
        #self.addLink(r1, r3, intfName1='r1-eth3', intfName2='r3-eth2', params1={'ip': '10.101.0.1/24'}, params2={'ip': '10.101.0.2/24'})
        #self.addLink(r2, r3, intfName1='r2-eth3', intfName2='r3-eth3', params1={'ip': '10.102.0.1/24'}, params2={'ip': '10.102.0.2/24'})
        
        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1',ip='10.1.0.10/24',defaultRoute='via 10.1.0.1')
        #h2 = self.addHost(name='h2',ip='10.1.0.20/24',defaultRoute='via 10.1.0.1')
        h3 = self.addHost(name='h3',ip='10.2.0.10/24',defaultRoute='via 10.2.0.1')
        #h4 = self.addHost(name='h4',ip='10.2.0.20/24',defaultRoute='via 10.2.0.1')
        #h5 = self.addHost(name='h5',ip='10.3.0.10/24',defaultRoute='via 10.3.0.1')
        #h6 = self.addHost(name='h6',ip='10.3.0.20/24',defaultRoute='via 10.3.0.1')
        # Add host-switch links
        self.addLink(h1, s1)
       # self.addLink(h2, s1)
        
        self.addLink(h3, s2)
        #self.addLink(h4, s2)
        
        #self.addLink(h5, s3)
        #self.addLink(h6, s3)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()

    # Add routing for reaching networks that aren't directly connected
    

    # type the following command in the mininet shell
    
    info(net['m'].cmd("ip route add 10.1.0.0/24 via 10.11.0.1 dev m-eth1"))
    info(net['m'].cmd("ip route add 10.2.0.0/24 via 10.12.0.1 dev m-eth1"))
    
    info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.10.0.1 dev r1-eth1"))
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.100.0.2 dev r1-eth2"))
    #info(net['r1'].cmd("ip route add 10.3.0.0/24 via 10.101.0.2 dev r1-eth3"))
    
    info(net['r2'].cmd("ip route add 10.1.0.0/24 via 10.100.0.1 dev r2-eth2"))
    #info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.102.0.2 dev r2-eth3"))
    
    #info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.101.0.1 dev r3-eth2"))
    #info(net['r3'].cmd("ip route add 10.2.0.0/24 via 10.102.0.1 dev r3-eth3"))
    net.startTerms()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()