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
        r1 = self.addHost('r1')
        
        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        # Add host-switch links in the same subnet

        self.addLink(r1,
                     s1,
                     intfName1='r1-eth1',
                     params1={'ip': '192.168.1.1/24'})

        self.addLink(r1,
                     s2,
                     intfName1='r1-eth2',
                     params1={'ip': '192.168.2.1/24'})
        


        # Adding hosts specifying the default route
        d1 = self.addHost(name='d1',
                          ip='172.168.1.10/24',
                          defaultRoute='via 192.168.1.1')
        d2 = self.addHost(name='d2',
                          ip='192.168.2.10/24',
                          defaultRoute='via 192.168.2.1')
        d3 = self.addHost(name='d3',
                          ip='172.168.1.20/24',
                          defaultRoute='via 172.168.1.1')
        
        d4 = self.addHost(name='d4',
                          ip='192.168.2.20/24',
                          defaultRoute='via 192.168.2.1')
        # Add host-switch links
        self.addLink(d1, s1)
        self.addLink(d3, s1)
        self.addLink(d2, s2)
        self.addLink(d4, s2)
        
def run():
    topo = NetworkTopo()

    net = Mininet(topo=topo)
    # Add routing for reaching networks that aren't directly connected
    #info(net['r1'].cmd("ip route add 10.1.0.0/24 via 10.0.0.1 dev r1-eth2"))
    #info(net['r1'].cmd("ip route add 10.0.0.0/24 via 10.1.0.1 dev r1-eth1"))

    #net.start()
    #CLI(net)
    #net.stop()


#if __name__ == '__main__':
    #setLogLevel('info')
    #topo = { 'mytopo': ( lambda: NetworkTopo() ) } 
    #run()
    