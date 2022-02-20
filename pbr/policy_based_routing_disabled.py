
#!/usr/bin/python


"""
linuxrouter.py: Example network with Linux IP router

This example converts a Node into a router using IP forwarding
already built into Linux.

The topology contains a router with three IP subnets:
 - 192.168.1.0/24 (interface IP: 192.168.1.1)
 - 172.16.0.0/12 (interface IP: 172.16.0.1)
 - 10.0.0.0/8 (interface IP: 10.0.0.1)

 It also contains three hosts, one in each subnet:
 - h1 (IP: 192.168.1.100)
 - h2 (IP: 172.16.0.100)
 - h3 (IP: 10.0.0.100)

 Routing entries can be added to the routing tables of the
 hosts or router using the "ip route add" or "route add" command.
 See the man pages for more details.

"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.util import irange

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        #self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        #self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class NetworkTopo( Topo ):
    "A simple topology of a router with three subnets (one host in each)."

    def build( self, n=2, h=1, **opts ):
        router = self.addNode( 'router', cls=LinuxRouter, ip='10.0.10.1/24' , inNamespace=False)
        host1 = self.addHost( 'host1', ip='10.0.10.2/24', defaultRoute='via 10.0.10.1' )
        host2 = self.addHost( 'host2', ip='10.0.11.2/24', defaultRoute='via 10.0.11.1' )
        server = self.addHost( 'server', ip='10.0.12.2/24')
        self.addLink( host1, router, intfName2='router-eth1', params2={ 'ip' : '10.0.10.1/24' } )
        self.addLink( host2, router, intfName2='router-eth2', params2={ 'ip' : '10.0.11.1/24' } )
        self.addLink( server, router, intfName2='router-eth3', params2={ 'ip' : '10.0.12.1/24' } )
        self.addLink( server, router,
                     intfName1='server-eth1', params1={ 'ip' : '10.0.13.2/24' },
                     intfName2='router-eth4', params2={ 'ip' : '10.0.13.1/24' })

def run():
    topo = NetworkTopo()
    #net = Mininet( topo=topo, controller=None ) # no controller needed
    from mininet.node import OVSController
    net = Mininet(topo = topo, controller = OVSController)

    net.start()
    net[ 'server' ].cmd( 'ifconfig lo:0 11.0.14.1/24 up')
    net[ 'server' ].cmd( 'ip route add 10.0.10.0/24 via 10.0.12.1')
    net[ 'server' ].cmd( 'ip route add 10.0.11.0/24 via 10.0.12.1')
    net[ 'router' ].cmd( 'route add -net 11.0.14.0/24 dev router-eth3')
    info( '*** Routing Table on Router\n' )
    print (net[ 'router' ].cmd( 'route -n' ))
    info( '*** Routing Table on Server\n' )
    print (net[ 'server' ].cmd( 'route -n' ))
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
