# Objective & Summary

In this lab, I will explore dynamic routing further.

_Lab Goals:_

- Observe differences between static and dynamic configurations.
- Analyze how dynamic routing adapts when a link is disabled.
- Record routing table changes using show ip route.

_Static Routing:_

- Manually configured routes.
- Useful for small networks or specific paths.
- Ensures full control but requires manual updates if the network changes.

_Dynamic Routing:_

- Uses protocols (like RIP, OSPF, or EIGRP) to automatically learn and update routes.
- Scales better for large networks.
- Adjusts routes dynamically in response to network changes.

# Key things learned

- The subnet 10.0.0.0/30 has only two usable IP addresses
  - The /30 notation means the subnet mask has 30 bits set to 1       (11111111.11111111.11111111.11111100, out of 32 bits)
  - 2 bits open means on 2^2 = 4 available options 10.0.0.0-3
  - the ip ending in 0 is the host address, and the one ending in 3 is the broadcast address so that leaves only the IPs ending with 1 and 2
- Topology types
  - Full mesh - direct connections between each router, good for LAN, smaller networks, not too scalable due to hardware limitations
  - Partial mesh - not all routers are directly connected, makes use of intermediate routers, less hardware/more real world realistic
  - hub and spoke - one router (hub) connects to the others (spokes), reduces complexity, hub fails whole system fails
- Port types matter, I initially had the router to switch connection through a switchport (layer 2), so I couldn't assign an IP through that interface
- configuring IPs for subnets between the routers is tricky:
  - R1 ↔ R2: 10.0.0.0/30
    - R1: 10.0.0.1
    - R2: 10.0.0.2
  - R2 ↔ R3: 10.0.0.4/30
    - R2: 10.0.0.5
    - R3: 10.0.0.6
  - The IPs 10.0.0.0 to 10.0.0.3 belong to the R1 ↔ R2 subnet (10.0.0.0/30) with useable IPs 10.0.0.1-2.
  - The IP 10.0.0.4 starts a new subnet (10.0.0.4/30) used for the R2 ↔ R3 connection with useable IPs 10.0.0.5-6.
  - Dynamic routing frees up the network administrator from having to set routes, this is key for scaling networks.

# Lab Setup for Static and Dynamic Routing

I have 3 networks:

Network A (192.168.1.0/24) connected to Router1.
Network B (192.168.2.0/24) connected to Router2.
Network C (192.168.3.0/24) connected to Router3.

Routers are interconnected.

Goal: Configure static routes first, then transition to dynamic routing using RIP or OSPF.

## Begin with static routing

#### 1. Static Topology:

- 3 routers (Router1, Router2, Router3) connected in a partial mesh with crossover cables. Cisco 1841 is selected
- 3 switches, one connected to each router. Cisco 2960 is selected
- 6 PCs, each connected to a switch.

![image](https://github.com/user-attachments/assets/bbb7ba46-8bd8-4de0-93e4-86a6c0405e92)


#### 2. Assign IP Addresses through DHCP:

Each router needs:

1. Interface to its local network:

Router1 to Network A: 192.168.1.1/24.
Router2 to Network B: 192.168.2.1/24.
Router3 to Network C: 192.168.3.1/24.

2. Interface to other routers (e.g., Router1 <-> Router2). Use a unique subnet, e.g., 10.0.0.0/30 for these links.

Step-by-step:

Setup each router's IP address and DHCP:

_CLI from router 1_

```
Router(config)#interface Fa0/0
Router(config-if)#ip address 192.168.1.1 255.255.255.0
Router(config-if)#no shutdown
Router(config-if)#
%LINK-5-CHANGED: Interface FastEthernet0/0, changed state to up
%LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to up
Router(config-if)#exit
Router(config)#ip dhcp pool PC_POOL
Router(dhcp-config)#network 192.168.1.0 255.255.255.0
Router(dhcp-config)#default-router 192.168.1.1
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
Router(config)#exit
```

After repeating this process for each router cluster, I verify that each PC has a correct IP assigned.

![image](https://github.com/user-attachments/assets/0cb9af1d-04f3-47ec-9af9-012678dfc97d)

Next, I need to configure the interfaces between routers.

_R1 to R2_

```
Router(config)# interface Fa0/1
Router(config-if)# ip address 10.0.0.1 255.255.255.252
Router(config-if)# no shutdown
Router(config-if)# exit
```

For R2 to R1, I would do "ip address 10.0.0.2 255.255.255.252"

For R2 to R3, "ip address 10.0.0.5 255.255.255.252" because 10.0.0.3-4 are a part of the subnet between R1 and R2

Once the interfaces are setup, I check to see if R1 can communicate with the other routers with "ping":

![image](https://github.com/user-attachments/assets/0e38170d-b0d4-49c3-b9b7-aeb588b3b6d1)

As expected, only the direct connection to R2 allows traffic.

When I try to ping PC3 from PC1, I get "Destination host unreachable".

#### 3. Static Routing Configuration:

Each router must know:

- How to reach the networks directly connected to the other routers.
- Use R2 as the intermediary router.

On R1:

- R2’s local network via R2’s IP 10.0.0.2:
  - ```Router(config)#ip route 192.168.2.0 255.255.255.0 10.0.0.2```
- R3’s local network via R2’s IP 10.0.0.2:
  - ```Router(config)#ip route 192.168.3.0 255.255.255.0 10.0.0.2```

On R3:

- R1’s local network via R2’s IP 10.0.0.5:
  - ```Router(config)#ip route 192.168.1.0 255.255.255.0 10.0.0.5```
- R2’s local network via R2’s IP 10.0.0.5:
  - ```Router(config)#ip route 192.168.2.0 255.255.255.0 10.0.0.5```

R2 needs to route traffic to:

- R1’s local network via R1’s IP 10.0.0.1:
  - ```Router(config)#ip route 192.168.1.0 255.255.255.0 10.0.0.1```
- R3’s local network via R3’s IP 10.0.0.6:
  - ```Router(config)#ip route 192.168.3.0 255.255.255.0 10.0.0.6```

Test connectivity:

Use ping from one PC to another across different networks.

PC1 to PC3

![image](https://github.com/user-attachments/assets/957e9c7b-7704-436b-9028-eeb590600c31)

PC1 to PC6

![image](https://github.com/user-attachments/assets/845a74d9-289c-4a1f-b2eb-3758d8883a8e)

PC3 to PC2 and PC3 to PC5

![image](https://github.com/user-attachments/assets/a5df6b0a-0add-4108-93dd-4173a122dbb0)

PC5 to PC1 and PC5 to PC4

![image](https://github.com/user-attachments/assets/0d31c64f-d8ad-42ef-8c9d-61ff3c96546a)

Success! Static routing is acheived! Next, I will go into dynamic routing.

## Dynamic Routing

Dynamic routing is a networking technique where routers automatically update and share information about the best paths for data to travel through a network, allowing them to adapt to changes in the network topology by choosing different routes based on current conditions.

I will use RIP (Routing Information Protocol).

Why Use RIP?

- RIP dynamically advertises all connected and learned networks to neighboring routers. This eliminates the need for manual static route configuration.
- If you expand the network or add new routers, RIP automatically propagates the new routes.

#### Topology

I will use the same topology from the static routing portion:

![image](https://github.com/user-attachments/assets/93348583-c8a2-42d2-b447-2eda868f57c3)


#### Steps

Configuring RIP on the routers:

On each of the routers (adjusting the 192.168.1.0 with their respective networks):

```
Router(config)#router rip
Router(config-router)#version 2
Router(config-router)#network 192.168.1.0
Router(config-router)#network 10.0.0.0
```

This tells each router to use RIP to route its packets. RIP version 2 supports subnet masks (classless routing), making it compatible with modern networks. The first line with the network command tells that router to advertise its network IP to the other routers using RIP and learn routes through other routers in this network (this case there are none). The second network line advertises the 10.0.0.0 IP to learn about routes from other routers on the same interface.


After this simple step, the routers should be connected and ready to send packets! But first I will remove the static routes set in the first part of this lab and verify RIP.

To remove the static routes I will use the same command to add the route but with "no" in front:

For example on router 1:

```
Router(config)#interface Fa0/1
Router(config-if)#no ip route 192.168.2.0 255.255.255.0
Router(config)#interface Fa0/1
Router(config-if)#no ip route 192.168.3.0 255.255.255.0
Router(config)#exit
```

And to check that only RIP is enabled and that R1 knows how to send traffic to R2 and R3:

```
Router#show ip route
Codes: C - connected, S - static, I - IGRP, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2, E - EGP
       i - IS-IS, L1 - IS-IS level-1, L2 - IS-IS level-2, ia - IS-IS inter area
       * - candidate default, U - per-user static route, o - ODR
       P - periodic downloaded static route

Gateway of last resort is not set

     10.0.0.0/30 is subnetted, 2 subnets
C       10.0.0.0 is directly connected, FastEthernet0/1
R       10.0.0.4 [120/1] via 10.0.0.2, 00:00:11, FastEthernet0/1
C    192.168.1.0/24 is directly connected, FastEthernet0/0
R    192.168.2.0/24 [120/1] via 10.0.0.2, 00:00:11, FastEthernet0/1
R    192.168.3.0/24 [120/2] via 10.0.0.2, 00:00:11, FastEthernet0/1
```

Note: it took some time for the router to learn the route to R3 (192.168.3.0), but we can see from R1s routing table that it knows how to send traffic without manually entering the route to Router 3!

Finally, I check for connectivity by pinging PCs among different networks. After managing an unexpected DHCP timeout for network 2, I get successful pings indicating RIP has been acheived.

PC1 to PC3 and PC5:

![image](https://github.com/user-attachments/assets/cc483c34-c003-47a2-b2f2-fb17ff84ab67)

