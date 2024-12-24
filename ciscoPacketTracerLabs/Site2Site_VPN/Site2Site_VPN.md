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

#### a. Configure IKE Phase 1 (ISAKMP Policy)
On both routers, configure the parameters for establishing the VPN tunnel.

Access ISAKMP Configuration Mode:

On both routers
```
Router(config)#crypto isakmp policy 10
```

Set Encryption, Hashing, Authentication, and Group:

On both routers
```
Router(config-isakmp)#encryption aes
Router(config-isakmp)#hash sha
Router(config-isakmp)#authentication pre-share
Router(config-isakmp)#group 2
Router(config-isakmp)#exit
```

Configure a Pre-Shared Key: This key must match on both routers.

On Router1
```
Router(config)#crypto isakmp key MySecretKey address 203.0.114.1
```

On Router2
```
Router(config)#crypto isakmp key MySecretKey address 203.0.113.1
```

#### b. Configure IKE Phase 2 (IPsec Transform Set)

The transform set defines how the data will be encrypted and authenticated.

Create the Transform Set:

```
Router(config)#crypto ipsec transform-set MyTransformSet esp-aes esp-sha-hmac
```

Repeat the same configuration on Router2.

Check for ISAKMP configurations and transform set:
```
Router#show crypto isakmp policy 

Global IKE policy
Protection suite of priority 10
        encryption algorithm:   AES - Advanced Encryption Standard (128 bit keys).
        hash algorithm:         Secure Hash Standard
        authentication method:  Pre-Shared Key
        Diffie-Hellman group:   #2 (1024 bit)
        lifetime:               86400 seconds, no volume limit
Default protection suite
        encryption algorithm:   DES - Data Encryption Standard (56 bit keys).
        hash algorithm:         Secure Hash Standard
        authentication method:  Rivest-Shamir-Adleman Signature
        Diffie-Hellman group:   #1 (768 bit)
        lifetime:               86400 seconds, no volume limit

Router#show crypto ipsec transform-set 
Transform set MyTransformSet: {    { esp-aes esp-sha-hmac  }
   will negotiate = { Tunnel,  },
```

#### c. Create the Crypto Map

The crypto map binds the VPN settings to a specific interface and defines the traffic to protect.

Define the Crypto Map:

```
Router(config)#crypto map MyCryptoMap 10 ipsec-isakmp
```

Set the Peer Address:

```
Router(config-crypto-map)#set peer 203.0.114.1
```

Specify the Transform Set:

```
Router(config-crypto-map)#set transform-set MyTransformSet
```

Define the Traffic to Protect (Access Control List): 

Create an access list to define the traffic between LAN1 and LAN2.

```
Router(config-crypto-map)#match address 101
```

Create the Access List:

```
Router(config)#access-list 101 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255
```

Repeat these steps on Router2, reversing the peer IP addresses and access list to reflect its LAN.

Verify map:

Router 1
```
Router#show crypto map
Crypto Map MyCryptoMap 10 ipsec-isakmp
        Peer = 203.0.114.1
        Extended IP access list 101
            access-list 101 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255
        Current peer: 203.0.114.1
        Security association lifetime: 4608000 kilobytes/3600 seconds
        PFS (Y/N): N
        Transform sets={
                MyTransformSet,
        }
        Interfaces using crypto map MyCryptoMap:
```

#### d. Apply the Crypto Map to the Interface

On both routers, apply the crypto map to the WAN interface:

Enter Interface Configuration Mode:

```
Router(config)#interface Fa0/1
```

Apply the Crypto Map:

```
Router(config-if)#crypto map MyCryptoMap
```

Repeat this on Router2.

Verify the interfaces:

```
Router#show crypto map 
Crypto Map MyCryptoMap 10 ipsec-isakmp
        Peer = 203.0.114.1
        Extended IP access list 101
            access-list 101 permit ip 192.168.1.0 0.0.0.255 192.168.2.0 0.0.0.255
        Current peer: 203.0.114.1
        Security association lifetime: 4608000 kilobytes/3600 seconds
        PFS (Y/N): N
        Transform sets={
                MyTransformSet,
        }
        Interfaces using crypto map MyCryptoMap:
                FastEthernet0/1
```

#### e. Verify the VPN

Ping Between PCs on LAN1 and LAN2: Test connectivity to ensure the VPN is functioning and traffic is encrypted.

The below is the result of pinging PC2 at site 2 from PC1 at site 1:

![image](https://github.com/user-attachments/assets/665f3fc9-0156-464d-ad50-69280e8a1a3f)

Great, we have connectivity. But what about security?

Check VPN Status: On both routers, run the following commands:

The QM_IDLE indicates that ISAKMP Phase 1 negotiation was successful.
```
Router#show crypto isakmp sa
IPv4 Crypto ISAKMP SA
dst             src             state          conn-id slot status
203.0.114.1     203.0.113.1     QM_IDLE           1010    0 ACTIVE
IPv6 Crypto ISAKMP SA
```

```
Router#show crypto ipsec sa
interface: FastEthernet0/1
    Crypto map tag: MyCryptoMap, local addr 203.0.113.1
   protected vrf: (none)
   local  ident (addr/mask/prot/port): (192.168.1.0/255.255.255.0/0/0)
   remote  ident (addr/mask/prot/port): (192.168.2.0/255.255.255.0/0/0)
   current_peer 203.0.114.1 port 500
    PERMIT, flags={origin_is_acl,}
   #pkts encaps: 7, #pkts encrypt: 7, #pkts digest: 0
   #pkts decaps: 6, #pkts decrypt: 6, #pkts verify: 0
   #pkts compressed: 0, #pkts decompressed: 0
   #pkts not compressed: 0, #pkts compr. failed: 0
   #pkts not decompressed: 0, #pkts decompress failed: 0
   #send errors 1, #recv errors 0
     local crypto endpt.: 203.0.113.1, remote crypto endpt.:203.0.114.1
     path mtu 1500, ip mtu 1500, ip mtu idb FastEthernet0/1
     current outbound spi: 0x2B4CF979(726464889)
     inbound esp sas:
      spi: 0xE7858BAD(3884288941)
        transform: esp-aes esp-sha-hmac ,
        in use settings ={Tunnel, }
        conn id: 2009, flow_id: FPGA:1, crypto map: MyCryptoMap
        sa timing: remaining key lifetime (k/sec): (4525504/3499)
        IV size: 16 bytes
        replay detection support: N
        Status: ACTIVE
     inbound ah sas:
     inbound pcp sas:
     outbound esp sas:
      spi: 0x2B4CF979(726464889)
        transform: esp-aes esp-sha-hmac ,
        in use settings ={Tunnel, }
        conn id: 2010, flow_id: FPGA:1, crypto map: MyCryptoMap
        sa timing: remaining key lifetime (k/sec): (4525504/3499)
        IV size: 16 bytes
        replay detection support: N
        Status: ACTIVE
     outbound ah sas:
     outbound pcp sas:
```

From the above output, the specific lines below show that the VPN is actually providing confidentiality for the traffic between tunnel:

```
   #pkts encaps: 7, #pkts encrypt: 7, #pkts digest: 0
   #pkts decaps: 6, #pkts decrypt: 6, #pkts verify: 0
```

Here, we see that the status for both is active and the security associations are valid. Thus the VPN tunnel is established!






