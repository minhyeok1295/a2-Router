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
        
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.1.0.1/24' )
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.2.0.1/24')
        r3 = self.addHost('r3', cls=LinuxRouter, ip='10.3.0.1/24')
        r4 = self.addHost('r4', cls=LinuxRouter, ip='10.4.0.1/24')
        r5 = self.addHost('r5', cls=LinuxRouter, ip='10.5.0.1/24')
        r6 = self.addHost('r6', cls=LinuxRouter, ip='10.6.0.1/24')
        r7 = self.addHost('r7', cls=LinuxRouter, ip='10.7.0.1/24')

        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        
        # Add host-switch links in the same subnet
        self.addLink(s1, r1, intfName2='r1-eth0', params2={'ip': '10.1.0.1/24'})
        self.addLink(s2, r2, intfName2='r2-eth0', params2={'ip': '10.2.0.1/24'})
        self.addLink(s3, r3, intfName2='r3-eth0', params2={'ip': '10.3.0.1/24'})
        self.addLink(s4, r4, intfName2='r4-eth0', params2={'ip': '10.4.0.1/24'})
        self.addLink(s5, r5, intfName2='r5-eth0', params2={'ip': '10.5.0.1/24'})
        self.addLink(s6, r6, intfName2='r6-eth0', params2={'ip': '10.6.0.1/24'})
        self.addLink(s7, r7, intfName2='r7-eth0', params2={'ip': '10.7.0.1/24'})
        
        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip': '10.11.0.1/24'}, params2={'ip': '10.11.0.2/24'})
        
        
        self.addLink(r2, r3, intfName1='r2-eth3', intfName2='r3-eth3', params1={'ip': '10.17.0.1/24'}, params2={'ip': '10.17.0.2/24'})
       
        
        self.addLink(r3, r4, intfName1='r3-eth4', intfName2='r4-eth4', params1={'ip': '10.22.0.1/24'}, params2={'ip': '10.22.0.2/24'})
       
        self.addLink(r4, r5, intfName1='r4-eth5', intfName2='r5-eth5', params1={'ip': '10.26.0.1/24'}, params2={'ip': '10.26.0.2/24'})
        
        self.addLink(r5, r6, intfName1='r5-eth6', intfName2='r6-eth6', params1={'ip': '10.29.0.1/24'}, params2={'ip': '10.29.0.2/24'})
        
        self.addLink(r6, r7, intfName1='r6-eth7', intfName2='r7-eth7', params1={'ip': '10.31.0.1/24'}, params2={'ip': '10.31.0.2/24'})        
        
        
        
        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1', ip='10.1.0.10/24', defaultRoute='via 10.1.0.1')
        h7 = self.addHost(name='h7', ip='10.7.0.10/24', defaultRoute='via 10.7.0.1')
        
        
        
        # Add host-switch links
        self.addLink(h1, s1)
        self.addLink(h7, s7)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()

    # Add routing for reaching networks that aren't directly connected

    # type the following command in the mininet shell
   
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.11.0.2 dev r1-eth2"))
    
    info(net['r2'].cmd("ip route add 10.1.0.0/24 via 10.11.0.1 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.17.0.2 dev r2-eth3"))
    
    info(net['r3'].cmd("ip route add 10.2.0.0/24 via 10.17.0.1 dev r3-eth3"))
    info(net['r3'].cmd("ip route add 10.4.0.0/24 via 10.22.0.2 dev r3-eth4"))  
    
    info(net['r4'].cmd("ip route add 10.3.0.0/24 via 10.22.0.1 dev r4-eth4"))  
    info(net['r4'].cmd("ip route add 10.5.0.0/24 via 10.26.0.2 dev r4-eth5"))
    
    
    info(net['r5'].cmd("ip route add 10.4.0.0/24 via 10.26.0.1 dev r5-eth5"))
    info(net['r5'].cmd("ip route add 10.6.0.0/24 via 10.29.0.2 dev r5-eth6"))
    
    info(net['r6'].cmd("ip route add 10.5.0.0/24 via 10.29.0.1 dev r6-eth6"))
    info(net['r6'].cmd("ip route add 10.7.0.0/24 via 10.31.0.2 dev r6-eth7"))


    info(net['r7'].cmd("ip route add 10.6.0.0/24 via 10.31.0.1 dev r7-eth7"))

    
    net.startTerms()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()