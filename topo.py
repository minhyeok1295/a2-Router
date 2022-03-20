
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.util import irange
# Reference http://csie.nqu.edu.tw/smallko/sdn/mininet_simple_router.html

class SimpleTopo(Topo):

    def build(self):
        # Simple Hosts, Swtiches and Router
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        '''
        h1 = self.addHost('h1', ip='192.168.1.1/24', mac="00:00:00:00:00:01")
        h2 = self.addHost('h2', ip='192.168.1.2/24', mac="00:00:00:00:00:02")
        h3 = self.addHost('h3', ip='192.168.1.3/24', mac="00:00:00:00:00:03")
        h4 = self.addHost('h4', ip='192.168.1.4/24', mac="00:00:00:00:00:04")
        '''
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
        
topos  = {'mytopo':(lambda:SimpleTopo())}

if __name__ == "__main__":
    setLogLevel('info')
    topo = SimpleTopo()
    net = Mininet(topo)
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("testing network connectivity")
    net.pingAll()
    net.stop()