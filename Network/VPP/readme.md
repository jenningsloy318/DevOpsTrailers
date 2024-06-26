VPP
---

The VPP platform is an extensible framework that provides out-of-the-box production quality switch/router functionality. It is the open source version of Cisco's Vector Packet Processing (VPP) technology: a high performance, packet-processing stack that can run on commodity CPUs.



- [VPP Wiki](https://wiki.fd.io/view/VPP)
- [VPP Use Cases](https://wiki.fd.io/view/vpp#Use_Cases)
- [vpp Doc](https://docs.fd.io/vpp/)
- [How To Connect A PCI Interface To VPP](https://wiki.fd.io/view/VPP/How_To_Connect_A_PCI_Interface_To_VPP)
## BVI Support
A bridge domain (BD) can have an L3 Bridge Virtual Interface (BVI) (one per BD) with multiple VXLAN-tunnels and Ethernet bridge ports. All three types of bridge ports (BVI, VXLAN and Ethernet) must interoperate properly to forward traffic to each other. BVI allow VMs on separate BDs or VXLAN segments to reach each other via IRB (Integrated Routing and Bridging).

The BVI for a BD is setup by creating and setup a loopback interface and then add it to the BD as its BVI interface. A BD in a VPP can only have one BVI. A VXLAN segment consists of multiple BDs from multiple VPPs, however, may have multiple BVIs with one BVI on each BD of each VPP.


## 1. Create two vlans and can be routable to each other
```sh{.line-numbers}

# Create a veth interface with one end named vpp-out(in vpp) and the other named vpp-host(on host vm)
# on host
ip link add name vpp2host type veth peer name host2vpp
ip link set dev vpp2host up
ip link set dev host2vpp up
ip addr add 10.10.1.1/24 dev host2vpp
ip route add 10.10.1.0/24 via 10.10.1.1
ip route add 192.168.10.0/24 via 10.10.1.2
ip route add 192.168.20.0/24 via 10.10.1.2


iptables -A FORWARD -i host2vpp -o ens33  -j ACCEPT
iptables -A FORWARD -i ens33 -o host2vpp -j ACCEPT
iptables -t nat -A POSTROUTING -o ens33 -j MASQUERADE

# on vpp
# Create a host interface attached to host2vpp.


vpp# create host-interface name vpp2host
vpp# set int ip address host-vpp2host 10.10.1.2/24
vpp# set int state host-vpp2host up
vpp# ip route add 0.0.0.0/0 via 10.10.1.1 host-vpp2host


# config bridge-domain 2 and interfaces
vpp# create bridge-domain 2
vpp# create loopback interface
vpp# set int l2 bridge loop0 2 bvi
vpp# set int ip address loop0 192.168.10.1/24 
vpp# set int state loop0 up
vpp# ip route add  192.168.10.0/24 via 192.168.10.1

vpp# create vhost socket /tmp/vm00.sock server
vpp# set int l2 bridge VirtualEthernet0/0/0 2
vpp# set int state VirtualEthernet0/0/0 up

# config bridge-domain 3 and interfaces

vpp# create bridge-domain 3
vpp# create loopback interface
vpp# set int l2 bridge loop1 3 bvi
vpp# set int ip address loop1 192.168.20.1/24 
vpp# set int state loop1 up
vpp# ip route add  192.168.20.0/24 via 192.168.20.1

vpp# create vhost socket /tmp/vm01.sock server
vpp# set int state VirtualEthernet0/0/1 up
vpp# set int l2 bridge VirtualEthernet0/0/1 3

# config acl 
vpp# set acl-plugin acl permit src 192.168.10.0/24, permit src 192.168.20.0/24,permit src 10.10.1.0/24
vpp# set acl-plugin acl deny all
vpp# show acl-plugin acl
vpp# set acl-plugin interface VirtualEthernet0/0/0  input acl 0
vpp# set acl-plugin interface VirtualEthernet0/0/1  input acl 0
vpp# set acl-plugin interface  loop0 input acl 0 
vpp# set acl-plugin interface  loop1 input acl 0  del ## delete acl 

```

- set acl-plugin interface <interface> <input|output> <acl INDEX> [del]
- set acl-plugin acl <permit|deny> src <PREFIX> dst <PREFIX> proto X sport X-Y dport X-Y [tag FOO] {use comma separated list for multiple rules}


## 2. XML content of the interface for libvirt 
```xml{.line-numbers}
    <interface type='vhostuser'>
      <source type='unix' path='/tmp/vm00.sock ' mode='server'/>
      <model type='virtio'/>
    </interface>

  ...

  <memoryBacking>
    <source type='memfd'/>
    <access mode='shared'/>
  </memoryBacking>

  ...

  <cpu mode='host-model' >
    <numa>
      <cell id='0' cpus='0-1' memory='4' unit='GiB' memAccess='shared'/>
    </numa>
  </cpu>
```

- portgroup works when the source of an interface is a network, but not sure vhostuser support portgroup



Links
- https://blog.csdn.net/Illina/article/details/88555425
- https://www.programmersought.com/article/54344042371/
- https://peiyake.com.cn/part1/vpp
- https://haryachyy.wordpress.com/2018/08/23/learning-vpp-internet-access/

reference
---

- tag-rewrite
  ```
  By default a subinterface has no tag-rewrite. To return a subinterface to this state use:

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 disable
  To pop vlan tags off packets received from a subinterface, use:

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 pop 1

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 pop 2
  To push one or two vlan tags onto packets received from an interface, use:

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 push dot1q 100

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 push dot1ad 100 150
  Tags can also be translated, which is basically a combination of a pop and push.

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 translate 1-1 dot1ad 100

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 translate 2-2 dot1ad 100 150

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 translate 1-2 dot1q 100

  vpp# set interface l2 tag-rewrite GigabitEthernet0/8/0.200 translate 2-1 dot1q 100 150
```