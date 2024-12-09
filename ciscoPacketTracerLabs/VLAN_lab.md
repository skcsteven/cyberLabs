# Objective / Summary

VLANs are a logical grouping of devices on a network that act as if they are on the same physical LAN, even if they are not physically connected to the same network segment. VLANs are used to segment a larger network into smaller, more manageable parts for improved performance, security, and organization.

I will be configuring a VLAN and exploring its features through Cisco Packet Tracer.

credits to: https://ipcisco.com/lesson/cisco-packet-tracer-vlan-configuration-example-ccna/

## Basic topology

Here is the configuration I will be working with:

![image](https://github.com/user-attachments/assets/9344d4ef-438a-4490-b938-6141a92e5c7a)

## Set up VLAN

First I will manually assign IPs to each of the PCs as the scope of this lab is VLAN.

Access ports are switch ports configured to belong to a single VLAN (Virtual Local Area Network). They are used to connect devices such as computers, printers, or phones to a specific VLAN. When a device communicates through an access port, the switch automatically assigns all traffic to the VLAN associated with that port.

1. We will set access ports that will access specific VLANs. We will do this with “switchport mode access” command under these interfaces.
2. We will also set the VLAN, that this port will access.
3. After that, we will set the trunk port that will carry multiple VLANs with “swithcport mode trunk” command.
4. Then we will also set this port with “no negotiate” command to prevent negotiation about the port role.
5. Laslty, we will set the allowed VLANs with “switchport trunk allowed vlan” command on this trunk and save our configuration.

_CLI inputs_

```
Switch>enable
Switch#show ip interface brief | include up
FastEthernet0/1        unassigned      YES manual up                    up 
FastEthernet0/2        unassigned      YES manual up                    up 
FastEthernet0/3        unassigned      YES manual up                    up 
FastEthernet0/4        unassigned      YES manual up                    up
Switch#configure terminal

Switch(config)#interface FastEthernet0/2
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 2
% Access VLAN does not exist. Creating vlan 2

Switch(config)#interface FastEthernet0/3
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 2

Switch(config-if)#interface FastEthernet0/4
Switch(config-if)#switchport mode access
Switch(config-if)#switchport access vlan 3

Switch(config-if)#interface FastEthernet0/1
Switch(config-if)#switchport mode trunk
Switch(config-if)#switchport nonegotiate

Switch(config-if)#switchport trunk allowed vlan 2-4
```

I will do the same process with the second switch.

## Check VLAN configuration

Our last step of VLAN Packet Tracer Example is configuration verification. to verify our VLAN Packet Tracer Configuration, we will use verification commands like “show vlan brief“, “show interfaces“, “show interfaces trunk” etc.

'''
Switch#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Fa0/5, Fa0/6, Fa0/7, Fa0/8
                                                Fa0/9, Fa0/10, Fa0/11, Fa0/12
                                                Fa0/13, Fa0/14, Fa0/15, Fa0/16
                                                Fa0/17, Fa0/18, Fa0/19, Fa0/20
                                                Fa0/21, Fa0/22, Fa0/23, Fa0/24
2    VLAN0002                         active    Fa0/2, Fa0/3
3    VLAN0003                         active    Fa0/4
1002 fddi-default                     active    
1003 token-ring-default               active    
1004 fddinet-default                  active    
1005 trnet-default                    active 
'''

This looks good, the PCs connected to the left switch are properly in their assigned VLAN. But the Fa0/1 connection to the other switch is not included. Now we will investigate each connection.

'''
Switch#show interfaces Fa0/1 switchport
Name: Fa0/1
Switchport: Enabled
Administrative Mode: trunk
Operational Mode: trunk
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: dot1q
Negotiation of Trunking: Off
Access Mode VLAN: 1 (default)
Trunking Native Mode VLAN: 1 (default)
Voice VLAN: none
Administrative private-vlan host-association: none
Administrative private-vlan mapping: none
Administrative private-vlan trunk native VLAN: none
Administrative private-vlan trunk encapsulation: dot1q
Administrative private-vlan trunk normal VLANs: none
Administrative private-vlan trunk private VLANs: none
Operational private-vlan: none
Trunking VLANs Enabled: 2-4
Pruning VLANs Enabled: 2-1001
Capture Mode Disabled
Capture VLANs Allowed: ALL
Protected: false
Appliance trust: none
'''

'''
Switch#show interfaces Fa0/2 switchport
Name: Fa0/2
Switchport: Enabled
Administrative Mode: static access
Operational Mode: static access
Administrative Trunking Encapsulation: dot1q
Operational Trunking Encapsulation: native
Negotiation of Trunking: Off
Access Mode VLAN: 2 (VLAN0002)
Trunking Native Mode VLAN: 1 (default)
Voice VLAN: none
Administrative private-vlan host-association: none
Administrative private-vlan mapping: none
Administrative private-vlan trunk native VLAN: none
Administrative private-vlan trunk encapsulation: dot1q
Administrative private-vlan trunk normal VLANs: none
Administrative private-vlan trunk private VLANs: none
Operational private-vlan: none
Trunking VLANs Enabled: All
Pruning VLANs Enabled: 2-1001
Capture Mode Disabled
Capture VLANs Allowed: ALL
Protected: false
Appliance trust: none
'''

'''
Switch#show interfaces trunk
Port        Mode         Encapsulation  Status        Native vlan
Fa0/1       on           802.1q         trunking      1

Port        Vlans allowed on trunk
Fa0/1       2-4

Port        Vlans allowed and active in management domain
Fa0/1       2,3

Port        Vlans in spanning tree forwarding state and not pruned
Fa0/1       2,3
'''

Interpreting the Output:
VLANs 2, 3, and 4 are allowed on the trunk, but only VLANs 2 and 3 are active and forwarding traffic.
VLAN 1 is the native VLAN for untagged traffic.
VLAN 4 is either not active in the management domain or is pruned due to VLAN pruning or STP rules.

## Verify communication

To verify the communication between same VLANs now we will use ping command to check the communication between two PCs in the same VLAN. Here, if the PCs are in the same VLAN, the ping will successfull. If they are in different VLANs, ping will not be successful.

From PC0 I will check the communication, the below results check out with the VLAN configuration because PC0 is able to connect to the other devices set to VLAN 2 and not those on VLAN 3.

'''
C:\>ipconfig

FastEthernet0 Connection:(default port)

   Connection-specific DNS Suffix..: 
   Link-local IPv6 Address.........: FE80::201:63FF:FE3E:7EA8
   IPv6 Address....................: ::
   IPv4 Address....................: 192.168.1.2
   Subnet Mask.....................: 255.255.255.0
   Default Gateway.................: ::
                                     192.168.1.1

Bluetooth Connection:

   Connection-specific DNS Suffix..: 
   Link-local IPv6 Address.........: ::
   IPv6 Address....................: ::
   IPv4 Address....................: 0.0.0.0
   Subnet Mask.....................: 0.0.0.0
   Default Gateway.................: ::
                                     0.0.0.0

C:\>ping 192.168.1.3

Pinging 192.168.1.3 with 32 bytes of data:

Reply from 192.168.1.3: bytes=32 time<1ms TTL=128
Reply from 192.168.1.3: bytes=32 time<1ms TTL=128
Reply from 192.168.1.3: bytes=32 time<1ms TTL=128
Reply from 192.168.1.3: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.1.3:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms

C:\>ping 192.168.1.4

Pinging 192.168.1.4 with 32 bytes of data:

Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 192.168.1.4:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),

C:\>ping 192.168.1.6

Pinging 192.168.1.6 with 32 bytes of data:

Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 192.168.1.6:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),

C:\>ping 192.168.1.7

Pinging 192.168.1.7 with 32 bytes of data:

Reply from 192.168.1.7: bytes=32 time<1ms TTL=128
Reply from 192.168.1.7: bytes=32 time<1ms TTL=128
Reply from 192.168.1.7: bytes=32 time<1ms TTL=128
Reply from 192.168.1.7: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.1.7:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms

C:\>ping 192.168.1.8

Pinging 192.168.1.8 with 32 bytes of data:

Reply from 192.168.1.8: bytes=32 time<1ms TTL=128
Reply from 192.168.1.8: bytes=32 time<1ms TTL=128
Reply from 192.168.1.8: bytes=32 time<1ms TTL=128
Reply from 192.168.1.8: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.1.8:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms
'''

I will now check that the other VLAN devices are connected properly.

'''
C:\>ping 192.168.1.6

Pinging 192.168.1.6 with 32 bytes of data:

Reply from 192.168.1.6: bytes=32 time<1ms TTL=128
Reply from 192.168.1.6: bytes=32 time<1ms TTL=128
Reply from 192.168.1.6: bytes=32 time<1ms TTL=128
Reply from 192.168.1.6: bytes=32 time<1ms TTL=128

Ping statistics for 192.168.1.6:
    Packets: Sent = 4, Received = 4, Lost = 0 (0% loss),
Approximate round trip times in milli-seconds:
    Minimum = 0ms, Maximum = 0ms, Average = 0ms

C:\>ping 192.168.1.7

Pinging 192.168.1.7 with 32 bytes of data:

Request timed out.
Request timed out.
Request timed out.
Request timed out.

Ping statistics for 192.168.1.7:
    Packets: Sent = 4, Received = 0, Lost = 4 (100% loss),
'''

The above shows that the devices on VLAN 3 are connected and no cross VLAN communication is possible.

## What I learned

_VLAN tagging_ is a process that adds a VLAN identifier (VLAN ID) to network frames (Ethernet packets) as they traverse a network. This tagging allows switches and other devices to know which VLAN the traffic belongs to, enabling proper segregation and routing of data in a network with multiple VLANs.

_Access Port vs. Trunk Port_

Access port carries traffic for one VLAN.	Removes VLAN tags before sending. Connection for end devices like PCs and printers.

Trunk Port keeps VLAN tags for identification. Carries traffic for multiple VLANs. Connection between switches or switch-router links.

The _switchport trunk nonegotiate_ command on a Cisco switch disables the Dynamic Trunking Protocol (DTP) for the specified interface. This means the port will not actively participate in the negotiation process to establish a trunk link with a connected device. Instead, it forces the port to remain in trunk mode without sending or responding to DTP packets.

Even if two devices are connected to the same switch, if they are set to different VLANs they won't have connectivity.
