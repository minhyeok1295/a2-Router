from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

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
        r1 = self.addHost('r1', cls=LinuxRouter, ip='10.0.0.1/24')
        r2 = self.addHost('r2', cls=LinuxRouter, ip='10.1.0.1/24')
        
        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        

        # Add host-switch links in the same subnet
        self.addLink(s1,
                     r1,
                     intfName2='r1-eth0',
                     params2={'ip': '10.0.0.1/24'})

        self.addLink(s2,
                     r1,
                     intfName2='r1-eth1',
                     params2={'ip': '10.0.1.1/24'})
        
        self.addLink(s3,
                     r2,
                     intfName2='r2-eth0',
                     params2={'ip': '10.1.0.1/24'})
        
        
        self.addLink(r1,
                     r2,
                     intfName1='r1-eth2',
                     intfName2='r2-eth1',
                     params1={'ip': '10.100.0.1/24'},
                     params2={'ip': '10.100.0.2/24'})
        
        
        

        # Adding hosts specifying the default route
        d1 = self.addHost(name='d1',
                          ip='10.0.0.10/24',
                          defaultRoute='via 10.0.0.1')
        d2 = self.addHost(name='d2',
                          ip='10.0.0.11/24',
                          defaultRoute='via 10.0.0.1')
        d3 = self.addHost(name='d3',
                          ip='10.0.1.10/24',
                          defaultRoute='via 10.0.1.1')
        d4 = self.addHost(name='d4',
                          ip='10.0.1.11/24',
                          defaultRoute='via 10.0.1.1')
        d5 = self.addHost(name='d5',
                          ip='10.1.0.10/24',
                          defaultRoute='via 10.1.0.1')
        d6 = self.addHost(name='d6',
                          ip='10.1.0.11/24',
                          defaultRoute='via 10.1.0.1')

        # Add host-switch links
        self.addLink(d1, s1)
        self.addLink(d2, s1)
        self.addLink(d3, s2)
        self.addLink(d4, s2)
        self.addLink(d5, s3)
        self.addLink(d6, s3)
def run():
    topo = NetworkTopo()

    net = Mininet(topo=topo)
    net.pingAll()
    # Add routing for reaching networks that aren't directly connected
    #info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.0.0.1 dev r1-eth2"))
    #info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.1.0.1 dev r1-eth1"))

    #net.start()
    #CLI(net)
    #net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    #topo = { 'mytopo': ( lambda: NetworkTopo() ) } 
    run()
    