### What I learned

- coaxial cable usage
- ipconfig, ipv4, ipv6, wireless vs ethernet, hierarchy of devices (server, modem, router/switch, end devices)
- subnet mask, default gateway

![image](https://github.com/user-attachments/assets/c474f396-d7a4-4ceb-b1c2-bb5f711b7159)

## Objectives
In this activity, I will build a simple network in Packet Tracer in the Logical Workspace.

Part 1: Build a Simple Network

Part 2: Configure the End Devices and Verify Connectivity

Instructions

Part 1: Build a Simple Network

In this part, you will build a simple network by deploying and connecting the network devices in the Logical Workspace.

Step 1: Add network devices to the workspace.

In this step, you will add a PC, laptop, and a cable modem to the Logical Workspace.

A cable modem is a hardware device that allows communications with an Internet Service Provider (ISP). The coaxial cable from the ISP is connected to the cable modem, and an Ethernet cable from the local network is also connected. The cable modem converts the coaxial connection to an Ethernet connection.

Using the Device-Type Selection Box, add the following devices to the workspace. The category and sub-category associated with the device are listed below:

=   PC: End Devices > End Devices > PC

=   Laptop: End Devices > End Devices > Laptop

=   Cable Modem: Network Devices > WAN Emulation > Cable Modem

Step 2: Change display names of the nework devices.

a.     To change the display names of the network devices, click the device icon in the Logical Workspace.

b.     Click the Config tab in the device configuration window.

c.     Enter the new name of the newly added device into the Display Name field: PC, Laptop, and Cable Modem.

Step 3: Add the physical cabling between devices on the workspace.

Using the Device-Type Selection Box, add the physical cabling between devices on the workspace.

a.     The PC will need a copper straight-through cable to connect to the wireless router. Using the Device-Type Selection Box, click Connections (lightning bolt icon). Select the copper straight-through cable in the Device-Specific Selection Box and attach it to the FastEthernet0 interface of the PC and the Ethernet 1 interface of the wireless router.

b.     The wireless router will need a copper straight-through cable to connect to the cable modem. Select the copper straight-through cable in the Device-Specific Selection Box and attach it to the internet interface of the wireless router and the Port 1 interface of the cable modem.

c.     The cable modem will need a Coaxial cable to connect to the internet cloud. Select the Coaxial cable in the Device-Specific Selection Box and attach it to the Port 0 interface of the cable modem and the Coaxial 7 interface of the internet cloud.

Part 2: Configure the End Devices and Verify Connectivity

In this part, you will connect a PC and a laptop to the Wireless router. The PC will be connected to the network using an Ethernet cable. For the Laptop, you will replace the wired Ethernet network interface card (NIC) with a wireless NIC and connect the Laptop to the router wirelessly.

After both end devices are connected to the network, you will verify connectivity to cisco.srv. The PC and the Laptop will each be assigned an IP (Internet Protocol) address. Internet Protocol is a set of rules for routing and addressing data on the internet. The IP addresses are used to identify the devices on a network and allow the devices to connect and transfer data on a network.

Step 1: Configure the PC.

You will configure the PC for the wired network in this step.

a.     Click the PC. In the Desktop tab, navigate to IP Configuration to verify that DHCP is enabled and the PC has received an IP address.

Select DHCP for the IP Configuration heading if you do not see an IP address for the IPv4 Address field. Observe the process as the PC is receiving an IP address from the DHCP server.

DHCP stands for dynamic host configuration protocol. This protocol assigns IP addresses to devices dynamically. In this simple network, the Wireless Router is configured to assign IP addresses to devices that request IP addresses. If DHCP is disabled, you will need to assign an IP address and configure all the necessary information to communicate with other devices on the network and the internet.

b.     Close IP Configuration. In the Desktop tab, click Command Prompt.

c.     At the prompt, enter ipconfig /all to review the IPv4 addressing information from the DHCP server. The PC should have received an IPv4 address in the 192.168.0.x range.

Note: There are two types of IP addresses: IPv4 and IPv6. An IPv4 (internet protocol version 4) address is a string of numbers in the form of x.x.x.x as you have been using in this lab. As the internet grew, the need for more IP addresses became necessary. So IPv6 (internet protocol version 6) was introduced in the late 1990s to address the limitations of IPv4. The details of IPv6 addressing are beyond the scope of this activity.

d.     Test connectivity to the cisco.srv from the PC. From the command prompt, issue the command ping cisco.srv. It may take a few seconds for the ping to return. Four replies should be received.

Step 2: Configure the Laptop.

In this step, you will configure the Laptop to access the wireless network.

a.     Click Laptop, and select the Physical tab.

b.     In the Physical tab, you will need to remove the Ethernet copper module and replace it with the Wireless WPC300N module.

1)    Power off Laptop by clicking the power button on the side of the laptop.

2)    Remove the currently installed Ethernet copper module by clicking on the module on the side of the laptop and dragging it to the MODULES pane on the left of the laptop window.

3)    Install the wireless WPC300N module by clicking it in the MODULES pane and dragging it to the empty module port on the side of the Laptop.

4)    Power on the Laptop by clicking the Laptop power button again.

c.     With the wireless module installed, connect the Laptop to the wireless network. Click the Desktop tab and select the PC Wireless.

d.     Select the Connect tab. After a slight delay, the wireless network HomeNetwork will be visible in the list of wireless networks. Click Refresh if necessary to see the list of available networks. Select the HomeNetwork. Click Connect.

e.     Close PC Wireless. Select Web Browser in the Desktop tab.

f.      In the Web Browser, navigate to cisco.srv.

The IP addresses for the end devices can range from 192.168.0.2 – 192.168.0.254. Each NIC will get a unique IP address in the same network.

The subnet mask is used to differentiate the host and the network ID portion of the IP address. You can relate the IP address to your street address. The subnet mask defines the length of the street name. The network part of the address is your street, 192.168.0. The house number is the host port of the IP address. For the IP address 192.168.0.2, the house number is 2 and the street is 192.168.0. If there is more than one house on the same street, for example, house number 3, will have an address 192.168.0.3. The maximum number of houses on this street is 253, ranging from 2 to 254.

The default gateway is analogous to the street intersection. The traffic from the 192.168.0 street has to exit through the intersection to another street. Another street is another network. In this network, default gateway is the wireless router that directs the traffic from the local network to the cable modem, and the traffic is then sent to the ISP.
