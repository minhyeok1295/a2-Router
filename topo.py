from mininet.topo import Topo
from mininet.node import Host, Node
# Reference http://csie.nqu.edu.tw/smallko/sdn/mininet_simple_router.html

class SimpleTopo(Topo):

    def build(self):
        # Simple Hosts, Swtiches and Router
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        h1 = self.addHost('h1')
        h1.setIP('127.0.0.1', 24)
        h2 = self.addHost('h2')
        h2.setIP('127.0.0.2', 24)
        h3 = self.addHost('h3')
        h3.setIP('127.0.0.3', 24)
        h4 = self.addHost('h4')
        h4.setIP('127.0.0.4', 24)
        r1 = self.addNode('r1')
        #Add Links
        self.addLink(h1,s1)
        self.addLink(h2,s1)
        self.addLink(h3,s2)
        self.addLink(h4,s2)
        self.addLink(s2,r1)
        self.addLink(s1,r1)
        
topos  = {'mytopo':(lambda:SimpleTopo())}
