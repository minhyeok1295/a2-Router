# -*- coding: utf-8 -*-

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
        
        m = self.addHost('m', cls=LinuxRouter, ip='10.0.0.1/24')
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.1.0.1/24' )
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.2.0.1/24')
        r3 = self.addHost('r3', cls=LinuxRouter, ip='10.3.0.1/24')
        r4 = self.addHost('r4', cls=LinuxRouter, ip='10.4.0.1/24')
        r5 = self.addHost('r5', cls=LinuxRouter, ip='10.5.0.1/24')
        r6 = self.addHost('r6', cls=LinuxRouter, ip='10.6.0.1/24')
        r7 = self.addHost('r7', cls=LinuxRouter, ip='10.7.0.1/24')

        # Add 2 switches
        sm = self.addSwitch('s0')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')
        
        # Add host-switch links in the same subnet
        self.addLink(sm, m, intfName2='m-eth0', params2={'ip': '10.0.0.1/24'})
        self.addLink(s1, r1, intfName2='r1-eth0', params2={'ip': '10.1.0.1/24'})
        self.addLink(s2, r2, intfName2='r2-eth0', params2={'ip': '10.2.0.1/24'})
        self.addLink(s3, r3, intfName2='r3-eth0', params2={'ip': '10.3.0.1/24'})
        self.addLink(s4, r4, intfName2='r4-eth0', params2={'ip': '10.4.0.1/24'})
        self.addLink(s5, r5, intfName2='r5-eth0', params2={'ip': '10.5.0.1/24'})
        self.addLink(s6, r6, intfName2='r6-eth0', params2={'ip': '10.6.0.1/24'})
        self.addLink(s7, r7, intfName2='r7-eth0', params2={'ip': '10.7.0.1/24'})
        
        # Add router-router link in a new subnet for the router-router connection
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip': '10.11.0.1/24'}, params2={'ip': '10.11.0.2/24'})
        self.addLink(r1, r3, intfName1='r1-eth3', intfName2='r3-eth2', params1={'ip': '10.12.0.1/24'}, params2={'ip': '10.12.0.2/24'})
        self.addLink(r1, r4, intfName1='r1-eth4', intfName2='r4-eth2', params1={'ip': '10.13.0.1/24'}, params2={'ip': '10.13.0.2/24'})
        self.addLink(r1, r5, intfName1='r1-eth5', intfName2='r5-eth2', params1={'ip': '10.14.0.1/24'}, params2={'ip': '10.14.0.2/24'})
        self.addLink(r1, r6, intfName1='r1-eth6', intfName2='r6-eth2', params1={'ip': '10.15.0.1/24'}, params2={'ip': '10.15.0.2/24'})
        self.addLink(r1, r7, intfName1='r1-eth7', intfName2='r7-eth2', params1={'ip': '10.16.0.1/24'}, params2={'ip': '10.16.0.2/24'})
        
        self.addLink(r2, r3, intfName1='r2-eth3', intfName2='r3-eth3', params1={'ip': '10.17.0.1/24'}, params2={'ip': '10.17.0.2/24'})
        self.addLink(r2, r4, intfName1='r2-eth4', intfName2='r4-eth3', params1={'ip': '10.18.0.1/24'}, params2={'ip': '10.18.0.2/24'})
        self.addLink(r2, r5, intfName1='r2-eth5', intfName2='r5-eth3', params1={'ip': '10.19.0.1/24'}, params2={'ip': '10.19.0.2/24'})
        self.addLink(r2, r6, intfName1='r2-eth6', intfName2='r6-eth3', params1={'ip': '10.20.0.1/24'}, params2={'ip': '10.20.0.2/24'})
        self.addLink(r2, r7, intfName1='r2-eth7', intfName2='r7-eth3', params1={'ip': '10.21.0.1/24'}, params2={'ip': '10.21.0.2/24'})
        
        self.addLink(r3, r4, intfName1='r3-eth4', intfName2='r4-eth4', params1={'ip': '10.22.0.1/24'}, params2={'ip': '10.22.0.2/24'})
        self.addLink(r3, r5, intfName1='r3-eth5', intfName2='r5-eth4', params1={'ip': '10.23.0.1/24'}, params2={'ip': '10.23.0.2/24'})
        self.addLink(r3, r6, intfName1='r3-eth6', intfName2='r6-eth4', params1={'ip': '10.24.0.1/24'}, params2={'ip': '10.24.0.2/24'})
        self.addLink(r3, r7, intfName1='r3-eth7', intfName2='r7-eth4', params1={'ip': '10.25.0.1/24'}, params2={'ip': '10.25.0.2/24'})
        
        self.addLink(r4, r5, intfName1='r4-eth5', intfName2='r5-eth5', params1={'ip': '10.26.0.1/24'}, params2={'ip': '10.26.0.2/24'})
        self.addLink(r4, r6, intfName1='r4-eth6', intfName2='r6-eth5', params1={'ip': '10.27.0.1/24'}, params2={'ip': '10.27.0.2/24'})
        self.addLink(r4, r7, intfName1='r4-eth7', intfName2='r7-eth5', params1={'ip': '10.28.0.1/24'}, params2={'ip': '10.28.0.2/24'})
        
        
        self.addLink(r5, r6, intfName1='r5-eth6', intfName2='r6-eth6', params1={'ip': '10.29.0.1/24'}, params2={'ip': '10.29.0.2/24'})
        self.addLink(r5, r7, intfName1='r5-eth7', intfName2='r7-eth6', params1={'ip': '10.30.0.1/24'}, params2={'ip': '10.30.0.2/24'})
        
        self.addLink(r6, r7, intfName1='r6-eth7', intfName2='r7-eth7', params1={'ip': '10.31.0.1/24'}, params2={'ip': '10.31.0.2/24'})        
        
        
        #connect all routers to monitor
        self.addLink(r1, m, intfName1='r1-eth1', intfName2='m-eth1', params1={'ip': '10.101.0.1/24'}, params2={'ip': '10.101.0.2/24'})
        self.addLink(r2, m, intfName1='r2-eth1', intfName2='m-eth2', params1={'ip': '10.102.0.1/24'}, params2={'ip': '10.102.0.2/24'})
        self.addLink(r3, m, intfName1='r3-eth1', intfName2='m-eth3', params1={'ip': '10.103.0.1/24'}, params2={'ip': '10.103.0.2/24'})
        self.addLink(r4, m, intfName1='r4-eth1', intfName2='m-eth4', params1={'ip': '10.104.0.1/24'}, params2={'ip': '10.104.0.2/24'})
        self.addLink(r5, m, intfName1='r5-eth1', intfName2='m-eth5', params1={'ip': '10.105.0.1/24'}, params2={'ip': '10.105.0.2/24'})
        self.addLink(r6, m, intfName1='r6-eth1', intfName2='m-eth6', params1={'ip': '10.106.0.1/24'}, params2={'ip': '10.106.0.2/24'})
        self.addLink(r7, m, intfName1='r7-eth1', intfName2='m-eth7', params1={'ip': '10.107.0.1/24'}, params2={'ip': '10.107.0.2/24'})
        
        
        
        # Adding hosts specifying the default route
        h1 = self.addHost(name='h1', ip='10.1.0.10/24', defaultRoute='via 10.1.0.1')
        h2 = self.addHost(name='h2', ip='10.2.0.10/24', defaultRoute='via 10.2.0.1')
        h3 = self.addHost(name='h3', ip='10.3.0.10/24', defaultRoute='via 10.3.0.1')
        h4 = self.addHost(name='h4', ip='10.4.0.10/24', defaultRoute='via 10.4.0.1')
        h5 = self.addHost(name='h5', ip='10.5.0.10/24', defaultRoute='via 10.5.0.1')
        h6 = self.addHost(name='h6', ip='10.6.0.10/24', defaultRoute='via 10.6.0.1')
        h7 = self.addHost(name='h7', ip='10.7.0.10/24', defaultRoute='via 10.7.0.1')
        
        
        
        # Add host-switch links
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(h4, s4)
        self.addLink(h5, s5)
        self.addLink(h6, s6)
        self.addLink(h7, s7)

def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()

    # Add routing for reaching networks that aren't directly connected

    # type the following command in the mininet shell
   
    info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.101.0.2 dev r1-eth1"))
    info(net['r1'].cmd("ip route add 10.2.0.0/24 via 10.11.0.2 dev r1-eth2"))
    info(net['r1'].cmd("ip route add 10.3.0.0/24 via 10.12.0.2 dev r1-eth3"))
    info(net['r1'].cmd("ip route add 10.4.0.0/24 via 10.13.0.2 dev r1-eth4"))
    info(net['r1'].cmd("ip route add 10.5.0.0/24 via 10.14.0.2 dev r1-eth5"))
    info(net['r1'].cmd("ip route add 10.6.0.0/24 via 10.15.0.2 dev r1-eth6"))
    info(net['r1'].cmd("ip route add 10.7.0.0/24 via 10.16.0.2 dev r1-eth7"))
    
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.102.0.2 dev r2-eth1"))
    info(net['r2'].cmd("ip route add 10.1.0.0/24 via 10.11.0.1 dev r2-eth2"))
    info(net['r2'].cmd("ip route add 10.3.0.0/24 via 10.17.0.2 dev r2-eth3"))
    info(net['r2'].cmd("ip route add 10.4.0.0/24 via 10.18.0.2 dev r2-eth4"))
    info(net['r2'].cmd("ip route add 10.5.0.0/24 via 10.19.0.2 dev r2-eth5"))
    info(net['r2'].cmd("ip route add 10.6.0.0/24 via 10.20.0.2 dev r2-eth6"))
    info(net['r2'].cmd("ip route add 10.7.0.0/24 via 10.21.0.2 dev r2-eth7"))
    
    info(net['r3'].cmd("ip route add 10.0.0.0/24 via 10.103.0.2 dev r3-eth1"))  
    info(net['r3'].cmd("ip route add 10.1.0.0/24 via 10.12.0.1 dev r3-eth2"))  
    info(net['r3'].cmd("ip route add 10.2.0.0/24 via 10.17.0.1 dev r3-eth3"))
    info(net['r3'].cmd("ip route add 10.4.0.0/24 via 10.22.0.2 dev r3-eth4"))  
    info(net['r3'].cmd("ip route add 10.5.0.0/24 via 10.23.0.2 dev r3-eth5"))
    info(net['r3'].cmd("ip route add 10.6.0.0/24 via 10.24.0.2 dev r3-eth6"))
    info(net['r3'].cmd("ip route add 10.7.0.0/24 via 10.25.0.2 dev r3-eth7"))
    
    
    info(net['r4'].cmd("ip route add 10.0.0.0/24 via 10.104.0.2 dev r4-eth1")) 
    info(net['r4'].cmd("ip route add 10.1.0.0/24 via 10.13.0.1 dev r4-eth2"))  
    info(net['r4'].cmd("ip route add 10.2.0.0/24 via 10.18.0.1 dev r4-eth3"))
    info(net['r4'].cmd("ip route add 10.3.0.0/24 via 10.22.0.1 dev r4-eth4"))  
    info(net['r4'].cmd("ip route add 10.5.0.0/24 via 10.26.0.2 dev r4-eth5"))
    info(net['r4'].cmd("ip route add 10.6.0.0/24 via 10.27.0.2 dev r4-eth6"))
    info(net['r4'].cmd("ip route add 10.7.0.0/24 via 10.28.0.2 dev r4-eth7"))
    
    
    
    info(net['r5'].cmd("ip route add 10.0.0.0/24 via 10.105.0.2 dev r5-eth1"))
    info(net['r5'].cmd("ip route add 10.1.0.0/24 via 10.14.0.1 dev r5-eth2"))  
    info(net['r5'].cmd("ip route add 10.2.0.0/24 via 10.19.0.1 dev r5-eth3"))
    info(net['r5'].cmd("ip route add 10.3.0.0/24 via 10.23.0.1 dev r5-eth4"))  
    info(net['r5'].cmd("ip route add 10.4.0.0/24 via 10.26.0.1 dev r5-eth5"))
    info(net['r5'].cmd("ip route add 10.6.0.0/24 via 10.29.0.2 dev r5-eth6"))
    info(net['r5'].cmd("ip route add 10.7.0.0/24 via 10.30.0.2 dev r5-eth7"))
    
    
    info(net['r6'].cmd("ip route add 10.0.0.0/24 via 10.106.0.2 dev r6-eth1"))
    info(net['r6'].cmd("ip route add 10.1.0.0/24 via 10.15.0.1 dev r6-eth2"))  
    info(net['r6'].cmd("ip route add 10.2.0.0/24 via 10.20.0.1 dev r6-eth3"))
    info(net['r6'].cmd("ip route add 10.3.0.0/24 via 10.24.0.1 dev r6-eth4"))  
    info(net['r6'].cmd("ip route add 10.4.0.0/24 via 10.27.0.1 dev r6-eth5"))
    info(net['r6'].cmd("ip route add 10.5.0.0/24 via 10.29.0.1 dev r6-eth6"))
    info(net['r6'].cmd("ip route add 10.7.0.0/24 via 10.31.0.2 dev r6-eth7"))


    info(net['r7'].cmd("ip route add 10.0.0.0/24 via 10.107.0.2 dev r7-eth1"))
    info(net['r7'].cmd("ip route add 10.1.0.0/24 via 10.16.0.1 dev r7-eth2"))  
    info(net['r7'].cmd("ip route add 10.2.0.0/24 via 10.21.0.1 dev r7-eth3"))
    info(net['r7'].cmd("ip route add 10.3.0.0/24 via 10.25.0.1 dev r7-eth4"))  
    info(net['r7'].cmd("ip route add 10.4.0.0/24 via 10.28.0.1 dev r7-eth5"))
    info(net['r7'].cmd("ip route add 10.5.0.0/24 via 10.30.0.1 dev r7-eth6"))
    info(net['r7'].cmd("ip route add 10.6.0.0/24 via 10.31.0.1 dev r7-eth7"))
    

    info(net['m'].cmd("ip route add 10.1.0.0/24 via 10.101.0.1 dev m-eth1"))
    info(net['m'].cmd("ip route add 10.2.0.0/24 via 10.102.0.1 dev m-eth2"))
    info(net['m'].cmd("ip route add 10.3.0.0/24 via 10.103.0.1 dev m-eth3"))
    info(net['m'].cmd("ip route add 10.4.0.0/24 via 10.104.0.1 dev m-eth4"))
    info(net['m'].cmd("ip route add 10.5.0.0/24 via 10.105.0.1 dev m-eth5"))
    info(net['m'].cmd("ip route add 10.6.0.0/24 via 10.106.0.1 dev m-eth6"))
    info(net['m'].cmd("ip route add 10.7.0.0/24 via 10.107.0.1 dev m-eth7"))
    
    
    net.startTerms()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()