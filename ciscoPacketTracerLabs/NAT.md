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

3. Enable NAT: 

  a. Configure NAT inside and outside interfaces:

  b. Configure a static NAT rule (example for one PC):

  c. For PAT (overload):

4. Configure Routing:

Ensure the router has a route to the external server/network:

4. Test NAT:

- From a PC, ping the external server (203.0.113.2).
- Use show ip nat translations on the router to verify NAT mappings.

5. Troubleshoot and Validate:

- Use Packet Tracer’s simulation mode to observe packet flow.
- Confirm that internal PCs can access external resources and vice versa (if static NAT is used for inbound traffic).









