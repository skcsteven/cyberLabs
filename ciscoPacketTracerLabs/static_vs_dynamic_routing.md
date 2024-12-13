# Objective & Summary

In this lab, I will explore dynamic routing further.

_Lab Goals:_

- Observe differences between static and dynamic configurations.
- Analyze how dynamic routing adapts when a link is disabled.
- Record routing table changes using show ip route.

_Static Routing:_

Manually configured routes.
Useful for small networks or specific paths.
Ensures full control but requires manual updates if the network changes.

_Dynamic Routing:_

Uses protocols (like RIP, OSPF, or EIGRP) to automatically learn and update routes.
Scales better for large networks.
Adjusts routes dynamically in response to network changes.



# Key things learned

- The subnet 10.0.0.0/30 has only two usable IP addresses
  - The /30 notation means the subnet mask has 30 bits set to 1       (11111111.11111111.11111111.11111100, out of 32 bits)
  - 2 bits open means on 2^2 = 4 available options 10.0.0.0-3
  - the ip ending in 0 is the host address, and the one ending in 3 is the broadcast address so that leaves only the IPs ending with 1 and 2
- 

# Lab Setup for Static and Dynamic Routing

I have 3 networks:

Network A (192.168.1.0/24) connected to Router1.
Network B (192.168.2.0/24) connected to Router2.
Network C (192.168.3.0/24) connected to Router3.

Routers are interconnected.

Goal: Configure static routes first, then transition to dynamic routing using RIP or OSPF.

## Begin with static routing

#### 1. Lab Topology:

- 3 routers (Router1, Router2, Router3). Cisco 2811 is selected with addition WIC card in order to have the required amount of ethernet ports
- 3 switches, one connected to each router. Cisco 2960 is selected
- 3 PCs, each connected to a switch.

#### 2. Assign IP Addresses:

Each router needs:

1. Interface to its local network:

Router1 to Network A: 192.168.1.1/24.
Router2 to Network B: 192.168.2.1/24.
Router3 to Network C: 192.168.3.1/24.

2. Interface to other routers (e.g., Router1 <-> Router2). Use a unique subnet, e.g., 10.0.0.0/30 for these links.

#### 3. Static Routing Configuration:

Access each router's CLI.

Manually add routes. For example, on Router1:

Router> enable
Router# configure terminal
Router(config)# ip route 192.168.2.0 255.255.255.0 10.0.0.2
Router(config)# ip route 192.168.3.0 255.255.255.0 10.0.0.6
This tells Router1 to send traffic for Network B and C to their respective neighboring routers.
Repeat for Router2 and Router3.

Test connectivity:

Use ping from one PC to another across different networks.
