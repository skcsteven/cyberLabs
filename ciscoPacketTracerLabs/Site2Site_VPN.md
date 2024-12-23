# Summary & Objectives

A Site-to-Site VPN connects two different networks securely over a public or untrusted network, like the internet. 

Lab Objectives:

- Secure communication between two networks using a VPN.
- Configure IPsec VPN on routers.
- Test connectivity between networks.

# What I learned

- Think of VPN as a secure tunnel rather than a type of proxy
-  to create a VPN tunnel between two devices, you need basic connectivity between them, meaning they must be able to communicate with each other on a network level, even if it's just a basic internet connection, in order to initiate the VPN connection and establish the secure tunnel for encrypted data transfer
-  Internet Security Association and Key Management Protocol (ISAKMP) is a protocol that establishes security associations and cryptographic keys in an internet environment. It's a key protocol in the IPsec (Internet Security) architecture
  - ISAKMP is used to: 
    - Negotiate, establish, modify, and delete Security Associations (SAs)
    - Create and manage peer authentication
    - Generate keys
    - Mitigate threats like Denial of Service (DoS) and anti-replay protection
  - ISAKMP operates in two phases:
    - Phase 1: Two ISAKMP servers agree on how to protect traffic between them. This agreement creates an ISAKMP SA.
    - Phase 2: The ISAKMP SA is used to negotiate further protocol SAs. 

# Topology Overview

- Router1: Represents Site A with LAN 192.168.1.0/24.
- Router2: Represents Site B with LAN 192.168.2.0/24.
- Both routers are connected via a simulated public network using a third router or cloud.

# Steps

## 1. _Set Up the Topology_

Use three routers:
- Router1: LAN side with a switch and end devices in the 192.168.1.0/24 subnet/configure DHCP.
```
Router(config)#interface Fa0/0
Router(config-if)#ip address 192.168.1.1 255.255.255.0
Router(config)#ip dhcp pool POOL
Router(dhcp-config)#network 192.168.1.0 255.255.255.0
Router(dhcp-config)#default-router 192.168.1.1
Router(dhcp-config)#dns-server 8.8.8.8
```
- Router2: LAN side with a switch and end devices in the 192.168.2.0/24 subnet/configure DHCP.
- Router3 or Cloud: Simulates the internet between Router1 and Router2.

Connect the routers:
- Use serial or Ethernet cables for connections between Router1, Router2, and Router3.
 
Assign IPs:
- Router1 WAN to Router3: 203.0.113.1/30
```
Router(config)#interface Fa0/1
Router(config-if)#ip address 203.0.113.1 255.255.255.252
Router(config-if)#no shutdown
```
- Router3 to Router1: 203.0.113.2/30
```
Router(config)#interface Fa0/0
Router(config-if)#ip address 203.0.113.2 255.255.255.252
Router(config-if)#no shutdown
Router(config-if)#exit
```
- Router2 WAN to Router3: 203.0.114.1/30
- Router3 to Router2: 203.0.114.2/30
```
Router#show ip interface b
Interface              IP-Address      OK? Method Status                Protocol 
FastEthernet0/0        203.0.113.2     YES manual up                    up 
FastEthernet0/1        203.0.114.2     YES manual up                    up 
Vlan1                  unassigned      YES unset  administratively down down
```

## 2. _Setup routing & Verify connectivity using ping between Router1 and Router2's WAN interfaces (through Router3)_

In the past lab I explored static vs dynamic routing. Here, I will use dynamic routing to simulate a WAN with much more routers and networks connected.

Setting up RIP:
```
Router(config)#router rip
Router(config-router)#version 2
Router(config-router)#network 192.168.1.0
Router(config-router)#network 203.0.113.0
Router(config-router)#exit
```
From this CLI on Router 1 we set it to use RIP, advertise its LAN network 192.168.1.0 and how to reach this network through its public facing IP 203.0.113.0.

On router 2, we follow similar steps but replacing the above with router 2's respective LAN and public IP.

On the internet-simulating router, RIP is setup differently:

```
Router(config)#router rip
Router(config-router)#version 2
Router(config-router)#network 203.0.113.0
Router(config-router)#network 203.0.114.0
Router(config-router)#exit
```

This pretty much listens and sends for routing information on the two networks above 203.0.113.0 and 203.0.114.0, thereby serving as a link or the medium that these two networks connect through.

Test to see if routing is successful by pinging PC2 from PC1:

![image](https://github.com/user-attachments/assets/4d3a7358-877a-425d-b6e8-b78fbba6bc13)

Looks good! Next up... VPN

## 3. _VPN Steps_

The objective is to create an IPsec tunnel.

a. Configure IKE Phase 1 (ISAKMP Policy)
On both routers, configure the parameters for establishing the VPN tunnel.

Access ISAKMP Configuration Mode:


Set Encryption, Hashing, Authentication, and Group:


Configure a Pre-Shared Key: This key must match on both routers.


On Router2:

b. Configure IKE Phase 2 (IPsec Transform Set)
The transform set defines how the data will be encrypted and authenticated.

Create the Transform Set:


Name the Transform Set and Exit:

Repeat the same configuration on Router2.

c. Create the Crypto Map
The crypto map binds the VPN settings to a specific interface and defines the traffic to protect.

Define the Crypto Map:


Set the Peer Address:


Specify the Transform Set:


Define the Traffic to Protect (Access Control List): 

Create an access list to define the traffic between LAN1 and LAN2.


Create the Access List:


Repeat these steps on Router2, reversing the peer IP addresses and access list to reflect its LAN.

d. Apply the Crypto Map to the Interface

On both routers, apply the crypto map to the WAN interface:

Enter Interface Configuration Mode:

Apply the Crypto Map:

Exit Configuration Mode:

Repeat this on Router2.

e. Verify the VPN

Ping Between PCs on LAN1 and LAN2: Test connectivity to ensure the VPN is functioning and traffic is encrypted.

Check VPN Status: On both routers, run the following commands:

Look for an active SA (Security Association) and encrypted packets.




