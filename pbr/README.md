
Pre-requisite:
apt-get install mininet.

In the newst versions of OVS, the ovs-controller was renamed to test-controller.

First install the openvswitch-testcontroller if you haven't with the following command:

 sudo apt-get install openvswitch-testcontroller
Second, create a symbolic link to the test-controller:

 sudo ln /usr/bin/ovs-testcontroller /usr/bin/controller 

Run:
sudo python3 policy_based_routing_disabled.py


on linux 
 watch "egrep router-eth.* /proc/net/dev"

 or 

netstat -i | grep router
router-e  1500       15      0      0 0            50      0      0      0 BMRU
router-e  1500       15      0      0 0            50      0      0      0 BMRU
router-e  1500       20      0      0 0            55      0      0      0 BMRU
router-e  1500        8      0      0 0            42      0      0      0 BMRU


mininet> host1 ping 11.0.14.1
mininet> host2 ping 11.0.14.1

Reference: https://chandanduttachowdhury.wordpress.com/2015/08/03/test-driving-policy-based-routing-on-linux/
