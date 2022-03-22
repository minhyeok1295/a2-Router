from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSKernelSwitch, UserSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink

net = Mininet( controller=RemoteController, link=TCLink, switch=OVSKernelSwitch )
h1 = net.addHost( 'h1', ip="10.0.1.10/24", mac="00:00:00:00:00:01" )
h2 = net.addHost( 'h2', ip="10.0.2.10/24", mac="00:00:00:00:00:02" )
h3 = net.addHost( 'h3', ip="10.0.1.20/24", mac="00:00:00:00:00:03" )
h4 = net.addHost( 'h4', ip="10.0.2.20/24", mac="00:00:00:00:00:04" )
r1 = net.addHost( 'r1')
s1 = net.addSwitch( 's1')
s2 = net.addSwitch( 's2')
c0 = net.addController( 'c0', controller=RemoteController, ip='127.0.0.1', port=6633 )
net.addLink( r1, s1 )
net.addLink( r1, s2 )
net.addLink( h1, s1 )
net.addLink( h3, s1 )
net.addLink( h2, s2 )
net.addLink( h4, s2 )
net.build()




topos = { 'mytopo': ( lambda: net.topos) } 