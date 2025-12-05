## LACP in Packet Tracer

This lab demonstrates port aggregation, LACP negotiation, and verifying the EtherChannel.

LACP (802.1ax/802.3ad) combines multiple Ethernet interfaces to operate as a single logical channel. 

Benefits:
- higher bandwidth
- load balancing
- redundancy
- simplicity of configuration

Active/Passive
- The "active" LACP initiates an LACP connection by sending LACPDUs
- The "passive" LACP will wait for the remote end to initiate the link.
- active can go with active
- passive must be with an active

Potential faults
- improper cabling
- duplex mismatch between port pairs
- incorrect active/passive configs

### Lab Setup

I will be using two switches to bundle two links into one logical port channel using LACP.

<img width="802" height="218" alt="image" src="https://github.com/user-attachments/assets/25ea4092-ed0a-4fd2-9c8b-dc9284e14b92" />

#### Configure LACP on the switches

First, I will configure one switch with active mode and the other with passive mode. After that, I will configure them both in active.

Switch 0 (active):
```
Switch0(config)# interface range g0/1 - 2
Switch0(config-if-range)# channel-group 1 mode active
Switch0(config-if-range)# switchport mode trunk
Switch0(config-if-range)# exit
```

Switch 1 (passive):
```
Switch1(config)# interface range g0/1 - 2
Switch1(config-if-range)# channel-group 1 mode passive
Switch1(config-if-range)# switchport mode trunk
Switch1(config-if-range)# exit
```

I also added PCs and management IPs to the switches for later verification:
```
Switch(config)#interface vlan 1
Switch(config-if)#ip address 192.168.1.2 255.255.255.0
```

#### Verify LACP

To confirm, LACP use "show etherchannel summary":

```
Switch#show etherchannel summary
Flags:  D - down        P - in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      f - failed to allocate aggregator
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port


Number of channel-groups in use: 1
Number of aggregators:           1

Group  Port-channel  Protocol    Ports
------+-------------+-----------+----------------------------------------------

1      Po1(SU)           LACP   Fa0/1(P) Fa0/2(P) 
```
