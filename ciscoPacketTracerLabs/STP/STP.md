# STP (Spanning Tree Protocol) Model in Packet Tracer

STP is a network protocol designed to prevent loops at the L2 level for networks with redundant links by logically blocking certain paths to create a single active path between any two devices.

Key characteristics of STP and how it works:
- Root Bridge - this is the switch that serves as a reference point for other switches to calculate shortest path two, it is found by choosing the switch with the lowest bridge ID (calculated by adding priority (multiple of 4096, default 32768), VLAN number and MAC address)
- Root port - selected port on every other switch that offers lowest cost path (shortest) to root bridge
- Designated port - selected port for each segment to carry traffic (downstream AWAY from root)
- Blocking ports - ports that dont forward traffic but listen for BDPUs
- BDPUs how the switches communicate to exchange info about bridge IDs/path costs/ and generally how to orient the network

## Topology

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

*Complete the same for switch 2, making sure correct port addresses*

## Verification of STP

To verify for spanning tree we can use the following command on any switch to confirm the root bridge of Switch 0:

```
s1#show spanning-tree 
VLAN0001
  Spanning tree enabled protocol ieee
  Root ID    Priority    24577
             Address     0007.ECBA.B834
             Cost        19
             Port        1(FastEthernet0/1)  ### This is the port to switch0
             Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec

  Bridge ID  Priority    32769  (priority 32768 sys-id-ext 1)
             Address     000A.F3EE.1C0E
             Hello Time  2 sec  Max Age 20 sec  Forward Delay 15 sec
             Aging Time  20

Interface        Role Sts Cost      Prio.Nbr Type
---------------- ---- --- --------- -------- --------------------------------
Fa0/3            Altn BLK 19        128.3    P2p
Fa0/1            Root FWD 19        128.1    P2p
Fa0/2            Desg FWD 19        128.2    P2p
```

Above we also see the blocking port to switch 1 on interface Fa0/3. This confirms that we have spanning tree enabled in our network, thus removing any redundant links. *Packet tracer also shows us graphically with an orange circle at the blocking port*

For double verification, I shut down the port from switch 1 to switch 2, wait some time and confirm that STP is functioning correctly as the same port gets blocked.

More useful commands:
- show spanning-tree vlan 1 — port roles, root bridge, cost, timers.
- show spanning-tree detail — detailed BPDU and timer info.
- show spanning-tree bridge — bridge ID info.
- show spanning-tree interface Gig0/1 detail — see state changes and edge-port info.
- show logging — see STP logs if DP/Root changes logged.
- show mac address-table dynamic — shows MAC learning per port.
- show interface status — up/down & speed/duplex issues.

PT's simulation mode lets us view the BPDUs and packets as the network learns and configures STP:

<img width="1098" height="622" alt="image" src="https://github.com/user-attachments/assets/80790253-575e-46b5-8eb8-66fbbc7c2286" />

## Additional Safety Options & Leaving remarks

Portfast - allows immediate forwarding for end devices (skips listening and learning)

BPDU Guard - if an access port that is portfast receives a BPDU it will be disabled to prevent loops
```
    interface (INTERFACE TO ACCESS)
    spanning-tree bpduguard enable
```
Root Guard - prevents other switches from becoming root
```
    interface (ports facing downstream switches)
    spanning-tree guard root
```
Loop guard - prevents against unidirectional link failures that can cause alternate ports to move to forwarding incorrectly
```   
    interface (non-designated ports)
    spanning-tree guard loop
```

When to use access or trunk port on a switch?
 - Switch ↔ PC → Access port
 - Switch ↔ Server (one VLAN) → Access port
 - Switch ↔ Switch → Trunk port
 - Switch ↔ Router for Router-on-a-Stick → Trunk port
 - Switch ↔ Firewall → Usually trunk (but depends on design)
