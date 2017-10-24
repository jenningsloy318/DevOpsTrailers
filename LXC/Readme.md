Description: Now we can use LXD to management the lxc containers, 

## Use bridge via openvswitch for lxc network, so install openvswitch first ##

Description:
    
   Use this method, containers are in a separate subnet, it can connect to ouside and other conainers on the same host, but outside network can't connect to it.

1. create network for container, this will also create a bridge on host and assign an ip address
```
lxc network create ovs-br0 bridge.driver=openvswitch
#  lxc network list
+---------+----------+---------+-------------+---------+
|  NAME   |   TYPE   | MANAGED | DESCRIPTION | USED BY |
+---------+----------+---------+-------------+---------+
| ens33   | physical | NO      |             | 0       |
+---------+----------+---------+-------------+---------+
| ovs-br0 | bridge   | YES     |             | 0       |
+---------+----------+---------+-------------+---------+

# lxc network show ovs-br0
config:
  bridge.driver: openvswitch
  ipv4.address: 10.28.250.1/24
  ipv4.nat: "true"
  ipv6.address: fd42:1692:bf5f:ad97::1/64
  ipv6.nat: "true"
description: ""
name: ovs-br0
type: bridge
used_by: []
managed: true

## ip addr show  ovs-br0
11: ovs-br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether 56:21:fe:0d:2d:45 brd ff:ff:ff:ff:ff:ff
    inet 10.28.250.1/24 scope global ovs-br0
       valid_lft forever preferred_lft forever
    inet6 fd42:1692:bf5f:ad97::1/64 scope global
       valid_lft forever preferred_lft forever
    inet6 fe80::5421:feff:fe0d:2d45/64 scope link
       valid_lft forever preferred_lft forever

```
2. create profile for LXC
```
# lxc profile  create ovs
```

3. attach the network to profile 

```
 #lxc network attach-profile ovs-br0 ovs eth0
 ```

4. add root disk 

```
# lxc profile device add ovs root 2 path=/ pool=default type=disk
```

5. show profile 
```
# lxc profile show ovs
config: {}
description: ""
devices:
  eth0:
    nictype: bridged
    parent: ovs-br0
    type: nic
  root:
    path: /
    pool: default
    type: disk
name: ovs
used_by: []
```

6. create a lxc container
```
#lxc launch ubuntu test -p ovs
#lxc info test
Name: test
Remote: unix://
Architecture: x86_64
Created: 2017/10/24 07:32 UTC
Status: Running
Type: persistent
Profiles: ovs
Pid: 7186
Ips:
  eth0: inet    10.28.250.77    veth4XLIF8
  eth0: inet6   fd42:1692:bf5f:ad97:216:3eff:fee1:d66d  veth4XLIF8
  eth0: inet6   fe80::216:3eff:fee1:d66d        veth4XLIF8
  lo:   inet    127.0.0.1
  lo:   inet6   ::1
Resources:
  Processes: 26
  CPU usage:
    CPU usage (in seconds): 5
  Memory usage:
    Memory (current): 95.52MB
    Memory (peak): 203.94MB
  Network usage:
    eth0:
      Bytes received: 13.31kB
      Bytes sent: 9.18kB
      Packets received: 98
      Packets sent: 72
    lo:
      Bytes received: 0B
      Bytes sent: 0B
      Packets received: 0
      Packets sent: 0
```

show host network:
```
#ip addr 
...
13: veth4XLIF8@if12: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue master ovs-system state UP group default qlen 1000
    link/ether fe:9e:a1:9c:ff:7a brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet6 fe80::fc9e:a1ff:fe9c:ff7a/64 scope link
       valid_lft forever preferred_lft forever
# ovs-vsctl show
94b48bf7-1005-4429-914a-db64f301b8d7
    Bridge "ovs-br0"
        Port "ovs-br0"
            Interface "ovs-br0"
                type: internal
        Port "veth1MAIFK"
            Interface "veth1MAIFK"
    ovs_version: "2.5.2"
```
### use host interface baased macvlan for lxc network ##

Description:
    
   Use this method, containers stays in the same lan with the host, they get ip address from outside network DHCP servers. using such kind of network, containers **can't** be accessed from the host.


1. create profile for lxc, the container macvlan network  interface is created on top of host ens33
    ```
    #lxc profile create macvlan
    #lxc profile device add  macvlan eth0 nic  nictype=macvlan  parent=ens33
    #lxc profile device add macvlan root 2 path=/ pool=default type=disk
    ```
2. create container
    ```
    #lxc info test2 -p macvlan
    Name: test2
    Remote: unix://
    Architecture: x86_64
    Created: 2017/10/24 09:29 UTC
    Status: Running
    Type: persistent
    Profiles: macvlan
    Pid: 2731
    Ips:
      eth0: inet    192.168.59.136
      eth0: inet6   fe80::216:3eff:fef0:f454
      lo:   inet    127.0.0.1
      lo:   inet6   ::1
    Resources:
      Processes: 28
      CPU usage:
        CPU usage (in seconds): 6
      Memory usage:
        Memory (current): 131.11MB
        Memory (peak): 250.02MB
      Network usage:
        lo:
          Bytes received: 0B
          Bytes sent: 0B
          Packets received: 0
          Packets sent: 0
        eth0:
          Bytes received: 1.21kB
          Bytes sent: 1.57kB
          Packets received: 10
          Packets sent: 15
    ```

3. test connection
    
    3.1 connect from host 
    ```
    #ssh 192.168.59.136
    ssh: connect to host 192.168.59.136 port 22: No route to host
    ```

    3.2 connect from outside, same lan with host
    ```
    ssh  192.168.59.136
    The authenticity of host '192.168.59.136 (192.168.59.136)' can't be established.
    ECDSA key fingerprint is SHA256:NRzsSok6ScaxVYK5XLH7omGMHN6zSvKSe/YNi/fjE6I.
    Are you sure you want to continue connecting (yes/no)?
```
### use macvlan baased macvlan for lxc network ##
Description:
    
   Use this method, containers stays in the same lan with the host, they get ip address from outside network DHCP servers. using this kind of network, containers can be accessed from the host

1. create macvlan interface on host 


    ```
    #ip link add link ens33 macvlan3 type macvlan mode bridge
    #ip link set macvlan3 up
    ```
    or add conf to `/etc/network/interfaces`
    ```
    auto macvlan3
    iface macvlan3 inet manual
    pre-up ip link add link ens33 macvlan3 type macvlan mode bridge
    ```


2. create profile for lxc, the container macvlan network interface is created on top of host macvlan3
    ```
    #lxc profile create macvlan3
    #lxc profile device add  macvlan3 eth0 nic  nictype=macvlan  parent=macvlan3
    #lxc profile device add macvlan3 root 2 path=/ pool=default type=disk
    ```

3. create lxc container

    ```
    #lxc  launch ubuntu test3 -p macvlan3
    #lxc info test3
    Name: test3
    Remote: unix://
    Architecture: x86_64
    Created: 2017/10/24 09:39 UTC
    Status: Running
    Type: persistent
    Profiles: macvlan3
    Pid: 2764
    Ips:
      eth0: inet    192.168.59.137
      eth0: inet6   fe80::216:3eff:fec2:a41
      lo:   inet    127.0.0.1
      lo:   inet6   ::1
    Resources:
      Processes: 26
      CPU usage:
        CPU usage (in seconds): 6
      Memory usage:
        Memory (current): 98.10MB
        Memory (peak): 234.65MB
      Network usage:
        eth0:
          Bytes received: 6.03kB
          Bytes sent: 3.88kB
          Packets received: 38
          Packets sent: 31
        lo:
          Bytes received: 0B
          Bytes sent: 0B
          Packets received: 0
          Packets sent: 0
    ```
4. add a route 

    ```
    #route add -host 192.168.59.137 dev macvlan3
    ```
5. access from host and outside the host (in same lan with the host)

    ```
    # ssh 192.168.59.137
    The authenticity of host '192.168.59.137 (192.168.59.137)' can't be established.
    ECDSA key fingerprint is SHA256:Kxc/tf2OMzln5obD5F8h6WmKtTBum844FmfH2vDdLdY.
    Are you sure you want to continue connecting (yes/no)?
    ```