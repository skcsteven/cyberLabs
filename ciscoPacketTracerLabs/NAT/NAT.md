# Objectives/Summary

In this lab, I will use cisco's packet tracer software to gain practical knowledge with NAT.

- Understand NAT Concepts: Gain familiarity with static, dynamic, and PAT (Port Address Translation).
- Configure NAT on a Router: Implement NAT to translate private IP addresses into public IPs for internet-bound traffic.
- Validate NAT Functionality: Test and verify that internal devices can communicate with external (simulated internet) devices.

Concepts learned:

- NAT occurs through the router and translate a set of IP addresses to different address - this helps preserve the limited amount of public IPv4 addresses
- Public vs Private IP addresses
  - public IP addresses are publicly registered on the internet and used to access internet
  - private IP addresses are not publicly registered and thus cannot access internet, only used internally (home or business)
  - multiple devices within a private sphere will have private ip addresses, these devices go through a router (NAT) with a public IP address to access the internet. NAT translates private to public, vice versa
- With IPv6, NAT will become obsolete
- A wildcard mask specifies which bits of an IP address must match when evaluating network traffic. It’s commonly used in ACLs to define ranges of IP addresses.
  - 0 in a bit position: Means that bit must match exactly.
  - 1 in a bit position: Means that bit can be anything (don’t care).
- Two routers must be on the same subnet to communicate
- Both NAT exceptions and port forwarding involve modifying the default behavior of Network Address Translation (NAT) to allow external devices to access specific internal devices.
  - A NAT exception allows specific inbound traffic from the external network to bypass the default NAT rules and reach a particular internal device.
  - Port forwarding is a specific kind of NAT exception. It tells the router to direct incoming traffic on a particular port (or set of ports) to a designated device within the private network.


# Lab setup

### Network Topology:

Devices:
- Router: Acts as the NAT device.
- Switch: Connects internal devices.
- Internal PCs: Simulate devices in a private network.
- Cloud or External Server: Simulates the internet (you can use a loopback or server).

IP Addressing:
- Private Network: Use the 192.168.1.0/24 range.
- Public Network: Use a public IP range like 203.0.113.0/24.

### Steps

1. Set Up the Topology:

- Connect PCs to the switch and the switch to the router's internal interface.
- Connect the router’s external interface to a "cloud" or an external server.

2. Assign IP Addresses:

- PCs in the private network: Assign IPs like 192.168.1.10 and 192.168.1.20 with a gateway of 192.168.1.1.
- Router:
  - Internal Interface (LAN): 192.168.1.1/24.
  - External Interface (WAN): 203.0.113.1/24.
- External Server: Assign 203.0.113.2/24.

_Configure router internal facing IP and DHCP for PCs_

```
Router(config)#interface Fa0/0
Router(config-if)#ip address 192.168.1.1 255.255.255.0
Router(config-if)#no shutdown
Router(config-if)#
%LINK-5-CHANGED: Interface FastEthernet0/0, changed state to up
%LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/0, changed state to up
Router(config-if)#exit
Router(config)#ip dhcp pool LOCAL_NETWORK
Router(dhcp-config)#network 192.168.1.0 255.255.255.0
Router(dhcp-config)#default-router 192.168.1.1
Router(dhcp-config)#dns-server 8.8.8.8
Router(dhcp-config)#exit
Router(config)#exit
```

_Set switchport mode to access for end devices_

```
Switch(config)#interface Fa0/2
Switch(config-if)#switchport mode access
```

Switch ports operate in "dynamic" mode by default, which means they attempt to negotiate a trunk link if connected to another device that supports it. This can cause unnecessary delays or connectivity issues if a port tries to operate as a trunk to a PC, which doesn't understand VLAN tagging. Configuring a port as access mode explicitly designates it as connecting to an end device like a PC. This ensures the port handles untagged traffic properly.

_Configure internet facing interface_

On private network router:
```
Router(config)#interface Fa0/1
Router(config-if)#ip address 203.0.113.1 255.255.255.252
Router(config-if)#no shutdown
```

On fake internet router:

```
Router(config)#interface Fa0/0
Router(config-if)#ip address 203.0.113.2 255.255.255.252
Router(config-if)#no shutdown
```

_Topology Image_

![image](https://github.com/user-attachments/assets/fad5a764-18e2-4769-9207-85443dd0f937)


After verifying DHCP assignment of IPs and connectivity between end devices and the router, we can proceed with NAT.

3. Enable NAT: 

I will use PAT (Port Address Translation), the most common type of NAT, to map multiple internal IPs to a single external IP.

  a. Configure NAT inside and outside interfaces:

  ```
  Router(config)#interface Fa0/0
  Router(config-if)#ip nat inside
  Router(config-if)#exit
  Router(config)#interface Fa0/1
  Router(config-if)#ip nat outside
  Router(config-if)#exit
  ```
  This step differentiates the internal IP address and the external, public, internet IP     address.
  
  b. Define the Private Network to Translate
  
  Create a standard access control list (ACL) to define which devices can use NAT (your internal private network):

  ```
  Router(config)# access-list 1 permit 192.168.1.0 0.0.0.255
  ```

  This ACL permits all devices in the 192.168.1.0/24 subnet to use NAT.

  c. Configure PAT (Dynamic NAT with Overload)
  
  Set up NAT to translate internal IP addresses to the router’s external IP address:

  ```
  Router(config)# ip nat inside source list 1 interface Fa0/1 overload
  ```
  This tells the router to take the access list 1 and translate their IPs to the IP address for interface Fa0/1 which is the public, cloud-facing IP. Overload is used to state that multiple internal IP addresses will be translated.

  d. Verify NAT configuration

  First, I have to ping the internet (router 2) from each of the devices in order for NAT to happen. After receiving successful pings on the PCs I check the NAT translations table on the router:

  ```
  Router#show ip nat translations
Pro  Inside global     Inside local       Outside local      Outside global
icmp 203.0.113.1:1024  192.168.1.4:1      203.0.113.2:1      203.0.113.2:1024
icmp 203.0.113.1:1025  192.168.1.4:2      203.0.113.2:2      203.0.113.2:1025
icmp 203.0.113.1:1026  192.168.1.4:3      203.0.113.2:3      203.0.113.2:1026
icmp 203.0.113.1:1027  192.168.1.4:4      203.0.113.2:4      203.0.113.2:1027
icmp 203.0.113.1:1     192.168.1.3:1      203.0.113.2:1      203.0.113.2:1
icmp 203.0.113.1:2     192.168.1.3:2      203.0.113.2:2      203.0.113.2:2
icmp 203.0.113.1:3     192.168.1.3:3      203.0.113.2:3      203.0.113.2:3
icmp 203.0.113.1:4     192.168.1.3:4      203.0.113.2:4      203.0.113.2:4
  ```

Here, we see that the local devices are correctly given outside addresses when connecting to the "internet". NAT is successful!
  
Because there are no NAT Exceptions (Port Forwarding), router 2 (internet) cannot single out a single PC on the local network that is behind router 1 because router 1's public-facing IP address represents each device behind it through NAT.








