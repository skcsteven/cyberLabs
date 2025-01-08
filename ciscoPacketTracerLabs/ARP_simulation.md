## ARP Simulation

I will use Packet Tracer's simulation mode to get an in-depth look at how ARP functions.

ARP connects IP addresses, which are dynamic and ever-changing, to MAC addresses, which are fixed and physical. This mapping is necessary because IP and MAC addresses are different lengths and are made up of different numbers in different orders. 

Before sending a packet, a host consults its ARP cache, which is a table of known IP and MAC addresses. ARP translates 32-bit IP addresses to 48-bit MAC addresses and vice versa. 

ARP is a critical function in the Internet protocol suite, as it allows hosts to reach the correct destination IP address. Without ARP, data can't flow between devices.

ARP requests are broadcast, while replies are unicast.

#### Network Topology

I will keep the topology simple to focus on ARP. 

My network will be two PCs each connected through a switch. IPs will be static and manually assigned: PC1 - 192.168.1.2, PC2 - 192.168.1.3

![image](https://github.com/user-attachments/assets/d568bbfa-e87c-4b79-a513-730a1097696c)

#### Simulate ARP Process

I will turn off all other filters in the Simulation Panel other than ARP.

![image](https://github.com/user-attachments/assets/d8a3fdbf-4304-42d4-8a57-566b6a5cc455)

First, I will ping PC2 from PC1:

![image](https://github.com/user-attachments/assets/7352160f-16d7-48e7-a224-52ea38b24820)

Clicking on the green envelope we can view the Outbound PDU (protocol data unit) details:

![image](https://github.com/user-attachments/assets/02d71f2c-0bcd-405e-bc41-dbc0f8d95960)

We can view the MAC for PC1 here and the target IP but the target MAC is unknown at this stage so it is in broadcast (target mac = 0000.0000.0000).

_1. OSI layer 1 - Encapsulate_

First , the ARP process constructs a request for the target IP address & the device encapsulates the PDU into an ethernet frame.

_2. OSI layer 1 - Transmit_

Next, PC1 sends out the frame

The PDU arrives at the switch next.

_3. OSI layer 2 - de-encapsulate_

The switch receives the frame.

_4. OSI layer 2 - Transfer_

a. The frame source MAC address does not exist in the MAC table of Switch. Switch adds a new MAC entry to its table.

b. The frame destination MAC address is broadcast. The Switch processes the frame.

c. The frame's destination MAC address matches the receiving port's MAC address, the broadcast address, or a multicast address.

d. The device decapsulates the PDU from the Ethernet frame.

e. The frame is an ARP frame. The ARP process processes it.

f. The active VLAN interface is not up. The ARP process ignores the frame.

_5. OSI layer 2 - encapsulate/transmit_

switch sends out the broadcast frame

The frame arrives at PC2

_6. OSI layer 2 - de-encapsulate/transfer_

PC2 de-encapsulates the frame, then:

a. The frame's destination MAC address matches the receiving port's MAC address, the broadcast address, or a multicast address.

b. The device decapsulates the PDU from the Ethernet frame.

c. The frame is an ARP frame. The ARP process processes it.

d. The ARP frame is a request.

e. The ARP request's target IP address matches the receiving port's IP address.

f. The ARP process updates the ARP table with received information.

_7. OSI layer 2 - encapsulate/transmit_

PC2 modifies the PDU with a new target (IP and MAC for PC1) and source (IP and MAC for PC2), then transmits:

![image](https://github.com/user-attachments/assets/8b36cd31-8e62-4697-ad8e-683f898b75fd)

Back at the switch.

_8. OSI layer 2 - de-encapsulate/transfer/encapsulate/transmit_

a. The frame source MAC address does not exist in the MAC table of 
Switch. Switch adds a new MAC entry to its table.

b. This is a unicast frame. Switch looks in its MAC table for the destination MAC address.

Finally, back at PC1:

_9. OSI layer 2 - de-encapsulate/accept_

a. The frame's destination MAC address matches the receiving port's MAC address, the broadcast address, or a multicast address.

b. The device decapsulates the PDU from the Ethernet frame.

c. The frame is an ARP frame. The ARP process processes it.

d. The ARP frame is a reply.

e. The ARP process updates the ARP table with received information.

f. The ARP process takes out and sends buffer packets waiting for this ARP reply.

#### Check ARP Tables

Using "arp -a" in the command prompt for PC1, we see that PC1 updated its ARP table with PC2's MAC information and internet address.

![image](https://github.com/user-attachments/assets/c6a6465f-1dad-4e4d-b74e-0d61cbe21d89)

We see the inverse when running the same command on PC2:

![image](https://github.com/user-attachments/assets/a6d58832-efb4-492b-926b-db8bbd294a9d)

