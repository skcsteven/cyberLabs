## STP (Spanning Tree Protocol) Model in Packet Tracer

STP is a network protocol designed to prevent loops at the L2 level for networks with redundant links by logically blocking certain paths to create a single active path between any two devices.

Key characteristics of STP and how it works:
- Root Bridge - this is the switch that serves as a reference point for other switches to calculate shortest path two, it is found by choosing the switch with the lowest bridge ID (calculated by adding priority (multiple of 4096, default 32768), VLAN number and MAC address)
- Root port - selected port on every other switch that offers lowest cost path (shortest) to root bridge
- Designated port - selected port for each segment to carry traffic (downstream AWAY from root)
- Blocking ports - ports that dont forward traffic but listen for BDPUs
- BDPUs how the switches communicate to exchange info about bridge IDs/path costs/ and generally how to orient the network

### Topology

<img width="560" height="587" alt="image" src="https://github.com/user-attachments/assets/ccb9022e-62d8-464a-b5a5-20864761c92d" />

### Configuring the switches for STP

First I will set up Switch0 as the root bridge by setting its priority value lower than the rest. After that I will configure the other two switches as non root by setting their priority value higher than Switch0's

#### Switch 0 config
```
enable
configure terminal
hostname s0

### verify open lines to the other switches
interface Fa0/1 
no shutdown
exit
interface Fa0/3
no shutdown
exit

### establish s0 as root by adjusting priority
spanning-tree vlan 1 priority 24576 # will be lower than rest

### configure IP addresses and open access port for PC0
interface Fa0/2
switchport mode access
switchport access vlan 1

### add IP to switch and manually to PC to ping from pc later to verify connectivity
interface vlan1
ip address 192.168.1.2 255.255.255.0
no shutdown

### commands to check for proper configurations
show ip interface b
show interface status
show vlan b
(pc0) ping 192.168.1.2
```

#### Switch 1 and 2 config

```
enable
configure t
hostname s2

### set management IP to ping later
interface vlan1
ip address 192.168.1.3 255.255.255.0
no shutdown
exit

### ensure open links to switch 0 and 2
interface Fa0/1
no shutdown
exit
interface Fa0/3
no shutdown
exit

### set access port to PC
interface Fa0/2
switchport mode access
switchport access vlan 1
no shutdown
exit

### verify connectivity by pinging each device
```
_Complete the same for switch 2, making sure correct port addresses

