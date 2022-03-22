from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info

from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
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
        h1 = self.addHost('h1', ip="10.0.1.10/24", mac="00:00:00:00:00:01")
        h2 = self.addHost('h2', ip="10.0.2.10/24", mac="00:00:00:00:00:02")
        h3 = self.addHost('h3', ip="10.0.1.20/24", mac="00:00:00:00:00:03")
        h4 = self.addHost('h4', ip="10.0.2.20/24", mac="00:00:00:00:00:04")
        r1 = self.addHost('r1')
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        c0 = self.addController('c0', controller=RemoteController, ip='127.0.0.1', port=8000)
        
        self.addLink(r1, s1)
        self.addLink(r1, s2)
        self.addLink(h1, s1)
        self.addLink(h3, s1)
        self.addLink(h2, s2)
        self.addLink(h4, s2)
        
        r1.cmd("ifconfig r1-eth0 0")
        r1.cmd("ifconfig r1-eth1 0")
        r1.cmd("ifconfig r1-eth0 hw etrher 00:00:00:00:01:01")
        r1.cmd("ifconfig r1-eth1 hw etrher 00:00:00:00:01:02")
        r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
        h1.cmd("ip route add default via 10.0.1.1")
        h2.cmd("ip route add default via 10.0.2.1")
        h3.cmd("ip route add default via 10.0.1.1")
        h4.cmd("ip route add default via 10.0.2.1")
        
        
        
        
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
    