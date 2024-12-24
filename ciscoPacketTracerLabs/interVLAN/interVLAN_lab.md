## Objective, Skills & Topics learned

In this lab, I will be configuring my own network in cisco's packet tracer to learn practical knowledge about interVLAN networking. 

Learned:
-  different interVLAN routing methods (router on a stick, layer 3 switch)
-  practical skills for setting up router, switch, and end devices (cisco commands, connection types, 802.1, trunk vs access)
-  DHCP and VLAN setup
-  Layer 3 switches are an incredible advancement in technology that reduces the need of a router on a stick for inter-VLAN routing
-  "routing" specifically means the communication between different networks or subnetworks, "switching" allows different end devices on the same network or subnetwork to communicate with each other

### Inter-VLAN Routing:

Routing is the process of directing data packets between different VLANs.
Routers or Layer 3 switches are used to facilitate communication between VLANs.

#### Routing Methods:

##### (1) Router-on-a-Stick:
A single physical interface on a router is configured with multiple subinterfaces, one for each VLAN.
The router performs the routing between VLANs by using the VLAN tags in the Ethernet frames.
Requires a trunk port on the switch to send tagged VLAN traffic to the router.

Steps:

- Configure subinterfaces on the router for each VLAN, assigning each subinterface an IP address in the corresponding VLAN's subnet.
- Configure the switch port connected to the router as a trunk port to carry traffic for all VLANs.
- Test inter-VLAN communication using ping or other tools.

My configuration:

![image](https://github.com/user-attachments/assets/1a1cdb55-e859-4dbe-8fc3-357fe9eed535)


Setup DHCP and VLANs on router:

_VLANs_
```
Router(config)#interface Gig0/0.10
Router(config-subif)#encapsulation dot1Q 10
Router(config-subif)#ip address 192.168.10.1 255.255.255.0
Router(config-subif)#no shutdown
Router(config-subif)#exit
Router(config)#interface Gig0/0.20
Router(config-subif)#
%LINK-5-CHANGED: Interface GigabitEthernet0/0.20, changed state to up

%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0.20, changed state to up

Router(config-subif)#encapsulation dot1Q 20
Router(config-subif)#ip address 192.168.20.1 255.255.255.0
Router(config-subif)#no shutdown
Router(config-subif)#exit
Router(config)#interface Gig0/0.30
Router(config-subif)#
%LINK-5-CHANGED: Interface GigabitEthernet0/0.30, changed state to up

%LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet0/0.30, changed state to up

Router(config-subif)#encapsulation dot1Q 30
Router(config-subif)#ip address 192.168.30.1 255.255.255.0
Router(config-subif)#no shutdown
Router(config-subif)#exit
```

_DHCP_

```
Router(config)#ip dhcp pool VLAN10
Router(dhcp-config)#network 192.168.10.0 255.255.255.0
Router(dhcp-config)#default-router 192.168.10.1
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
Router(config)#ip dhcp pool VLAN20
Router(dhcp-config)#network 192.168.20.0 255.255.255.0
Router(dhcp-config)#default-router 192.168.20.1
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
Router(config)#ip dhcp pool VLAN30
Router(dhcp-config)#network 192.168.30.0 255.255.255.0
Router(dhcp-config)#default-router 192.168.30.1
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
```

_Check for VLANs and DHCP Pools_

```
Router#show running-config | section interface
interface GigabitEthernet0/0
 no ip address
 duplex auto
 speed auto
interface GigabitEthernet0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
interface GigabitEthernet0/0.20
 encapsulation dot1Q 20
 ip address 192.168.20.1 255.255.255.0
interface GigabitEthernet0/0.30
 encapsulation dot1Q 30
 ip address 192.168.30.1 255.255.255.0
interface GigabitEthernet0/1
 no ip address
 duplex auto
 speed auto
 shutdown
interface Vlan1
 no ip address
 shutdown
Router#show running-config | section ip dhcp pool
ip dhcp pool VLAN10
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
ip dhcp pool VLAN20
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1
 dns-server 8.8.8.8
ip dhcp pool VLAN30
 network 192.168.30.0 255.255.255.0
 default-router 192.168.30.1
 dns-server 8.8.8.8
```

Next I need to set up trunking between the router and switch as well as the separate VLANs for each PC:

```
Switch#config
Configuring from terminal, memory, or network [terminal]? terminal
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#interface Gig0/1
Switch(config-if)#switchport mode trunk

Switch(config-if)#interface Fa0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#interface Fa0/2
Switch(config-if)#switchport mode access
Switch(config-if)#switchport acces vlan 20
Switch(config-if)#interface Fa0/3
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 30

```

Check to see if all good:

```
Switch#show vlan b

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/4, Fa0/5, Fa0/6, Fa0/7
                                                Fa0/8, Fa0/9, Fa0/10, Fa0/11
                                                Fa0/12, Fa0/13, Fa0/14, Fa0/15
                                                Fa0/16, Fa0/17, Fa0/18, Fa0/19
                                                Fa0/20, Fa0/21, Fa0/22, Fa0/23
                                                Fa0/24, Gig0/2
10   VLAN0010                         active    Fa0/1
20   VLAN0020                         active    Fa0/2
30   VLAN0030                         active    Fa0/3
1002 fddi-default                     active    
1003 token-ring-default               active    
1004 fddinet-default                  active    
1005 trnet-default                    active

Switch#show interface trunk
Port        Mode         Encapsulation  Status        Native vlan
Gig0/1      on           802.1q         trunking      1

Port        Vlans allowed on trunk
Gig0/1      1-1005

Port        Vlans allowed and active in management domain
Gig0/1      1,10,20,30

Port        Vlans in spanning tree forwarding state and not pruned
Gig0/1      1,10,20,30

Router#show ip dhcp binding
IP address       Client-ID/              Lease expiration        Type
                 Hardware address
192.168.10.2     0002.17D1.3CD2           --                     Automatic
192.168.20.2     00D0.FF92.111C           --                     Automatic
192.168.30.2     0003.E4E8.A76D           --                     Automatic
```

Now, I will enable DHCP for each PC and ensure that it gets a correct IP:

![image](https://github.com/user-attachments/assets/a60edf4b-184d-415c-affb-29cd4d58b84d)

Finally, to check if interVLAN networking is acheived...

_results from PC1 pinging the other two PCs on different VLANs_
![image](https://github.com/user-attachments/assets/41b53293-6ce8-4673-b99f-74114b8be091)

Success! The other PCs also are able to communicate into the different VLANs.

One side note for further investigation is why the first request failed when first pinging a different VLANs device.



##### (2) Layer 3 Switch:
A Layer 3 switch combines the functionality of a switch and a router.
VLANs are configured on the switch, and SVIs (Switch Virtual Interfaces) are used for routing.
Traffic between VLANs is routed directly within the switch, improving performance.

![image](https://github.com/user-attachments/assets/e1937ba0-3515-4fd7-ba40-34d7ff4f6eb6)

Steps:

- Create VLANs and assign ports to them.
- Enable routing on the Layer 3 switch.
- Configure an SVI for each VLAN with an IP address to act as the default gateway for devices in that VLAN.
- Setup DHCP to assign IPs for end devices
- Test communication between VLANs.

First, I need to configure my switch (VLANs, routing).

VLAN creation
```
Switch>enable
Switch#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#vlan 10
Switch(config-vlan)#exit
Switch(config)#vlan 20
Switch(config-vlan)#exit
Switch(config)#vlan 30
Switch(config-vlan)#exit
Switch(config)#exit

Switch#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/1, Fa0/2, Fa0/3, Fa0/4
                                                Fa0/5, Fa0/6, Fa0/7, Fa0/8
                                                Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                Fa0/13, Fa0/14, Fa0/15, Fa0/16
                                                Fa0/17, Fa0/18, Fa0/19, Fa0/20
                                                Fa0/21, Fa0/22, Fa0/23, Fa0/24
                                                Gig0/1, Gig0/2
10   VLAN0010                         active    
20   VLAN0020                         active    
30   VLAN0030                         active    
1002 fddi-default                     active    
1003 token-ring-default               active    
1004 fddinet-default                  active    
1005 trnet-default                    active 
```

Enable routing:

```
Switch(config)#ip routing
```

Create and configure Switch Virtual Interfaces (SVIs) for each VLAN. These will act as the gateway for devices in each VLAN:

```
Switch(config)#interface vlan 10
Switch(config-if)#
%LINK-5-CHANGED: Interface Vlan10, changed state to up

Switch(config-if)#ip address 192.168.10.1 255.255.255.0
Switch(config-if)#no shutdown
Switch(config-if)#exit
Switch(config)#interface vlan 20
Switch(config-if)#
%LINK-5-CHANGED: Interface Vlan20, changed state to up

Switch(config-if)#ip address 192.168.20.1 255.255.255.0
Switch(config-if)#no shutdown
Switch(config-if)#exit
Switch(config)#interface vlan 30
Switch(config-if)#
%LINK-5-CHANGED: Interface Vlan30, changed state to up

Switch(config-if)#ip address 192.168.30.1 255.255.255.0
Switch(config-if)#no shutdown
Switch(config-if)#exit
```

Setup DHCP:

```
Switch(config)#ip dhcp pool VLAN0010
Switch(dhcp-config)#network 192.168.10.0 255.255.255.0
Switch(dhcp-config)#default-router 192.168.10.1
Switch(dhcp-config)#exit
Switch(config)#ip dhcp pool VLAN0020
Switch(dhcp-config)#network 192.168.20.0 255.255.255.0
Switch(dhcp-config)#default-router 192.168.20.1
Switch(dhcp-config)#exit
Switch(config)#ip dhcp pool VLAN0030
Switch(dhcp-config)#network 192.168.30.0 255.255.255.0
Switch(dhcp-config)#default-router 192.168.30.1
Switch(dhcp-config)#exit
```
 Exclude SVI addresses from dhcp:
```
Switch(config)#ip dhcp excluded-address 192.168.10.1
Switch(config)#ip dhcp excluded-address 192.168.20.1
Switch(config)#ip dhcp excluded-address 192.168.30.1
```

Add endpoint devices and connect to VLANs:

```
Switch(config)#interface Fa0/1
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 10
Switch(config-if)#
%LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to up

Switch(config-if)#exit
Switch(config)#interface Fa0/2
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 20
Switch(config-if)#
%LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to up

Switch(config-if)#exit
Switch(config)#interface Fa0/3
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 30
Switch(config-if)#
%LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan30, changed state to up

Switch(config-if)#exit
Switch(config)#exit
Switch#
%SYS-5-CONFIG_I: Configured from console by console

Switch#show vlan b

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/4, Fa0/5, Fa0/6, Fa0/7
                                                Fa0/8, Fa0/9, Fa0/10, Fa0/11
                                                Fa0/12, Fa0/13, Fa0/14, Fa0/15
                                                Fa0/16, Fa0/17, Fa0/18, Fa0/19
                                                Fa0/20, Fa0/21, Fa0/22, Fa0/23
                                                Fa0/24, Gig0/1, Gig0/2
10   VLAN0010                         active    Fa0/1
20   VLAN0020                         active    Fa0/2
30   VLAN0030                         active    Fa0/3
1002 fddi-default                     active    
1003 token-ring-default               active    
1004 fddinet-default                  active    
1005 trnet-default                    active    
```

After enabling DHCP IP assignment for each PC, I will test to see if interVLAN communication is acheived with the ping command between the PCs:

![image](https://github.com/user-attachments/assets/f5f631b9-bcb5-4c31-a0ac-098229664b12)


Success!
