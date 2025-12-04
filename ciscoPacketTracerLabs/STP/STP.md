## STP (Spanning Tree Protocol) Model in Packet Tracer

STP is a network protocol designed to prevent loops at the L2 level for networks with redundant links by logically blocking certain paths to create a single active path between any two devices.

Key characteristics of STP and how it works:
- Root Bridge - this is the switch that serves as a reference point for other switches to calculate shortest path two, it is found by choosing the switch with the lowest bridge ID (calculated by adding priority, VLAN number and MAC address)
- Root port - selected port on every other switch that offers lowest cost path (shortest) to root bridge
- Designated port - selected port for each segment to carry traffic (downstream AWAY from root)
- Blocking ports - ports that dont forward traffic but listen for BDPUs
- BDPUs how the switches communicate to exchange info about bridge IDs/path costs/ and generally how to orient the network

My topology to demonstrate STP:

------

