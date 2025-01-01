# Raspberry Pi DNS Server

In this home lab, I set up my own DNS server with a Rapsberry Pi model 3B to learn practical networking skills. My Pi is connected via ethernet directly to my home router and I perform all configurations headless by SSHing into the pi from another device. I will make use of DNSMASQ on my Pi to provide DNS services.

## Steps

#### 1. Set up static IP address on Raspberry Pi

I set a static IP address for my pi so that connecting devices configured to the DNS service are actually able to look for the right server. This entails changing the /etc/dhcpcd.conf file. This file is used by devices to specify how they handle IP assignment.

First, I find my home networks useable IP range:

```
jonah@raspberrypi:~ $ ifconfig
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.153  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::99d5:9397:5496:6534  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:95:31:be  txqueuelen 1000  (Ethernet)
        RX packets 65290  bytes 12303515 (11.7 MiB)
        RX errors 0  dropped 81  overruns 0  frame 0
        TX packets 1213  bytes 121390 (118.5 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

Looking at eth0, I see that my workable IP range is 192.168.1.1-255. But to avoid using IP addresses assigned to my gateway or other devices, I will just configure my static IP address to be the one that was already assigned to the Pi by DHCP.

Now, I edit the /etc/dhcpcd.conf file with:

```
interface eth0
static ip_address=192.168.1.153  # Set your desired static IP
static routers=192.168.1.1          # Your router's IP
static domain_name_servers=8.8.8.8  # DNS server (Google DNS in this case)
```

For this to take effect, restart the DHCP client service:

```
sudo systemctl restart dhcpcd
```

#### 2. Install and Configure dnsmasq

First, I install dnsmasq:
```
sudo apt update
sudo apt install dnsmasq -y
```

Next, I need to update the .conf file to set the configurations for the DNS server. To do this, I will backup the original and make a new one with my desired configurations:

```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
sudo nano /etc/dnsmasq.conf
```

new /etc/dnsmasq.conf
```
# Listen on the Ethernet interface
interface=eth0

# Set upstream DNS servers (e.g., Cloudflare and Google)
server=1.1.1.1
server=8.8.8.8

# Disable reading /etc/resolv.conf for upstream servers
no-resolv

# Enable logging for DNS queries
log-queries

# Optional: Add custom blocklist
addn-hosts=/etc/hosts.blocklist
```

For my DNS server, I am also adding a blocklist. Whenever traffic from or to the entries on the blocklist go through the DNS server, the server will black hole them. This step is below.

#### 3. Create a Blocklist

In the above /etc/dnsmasq.conf file, we specified a blocklist of /etc/hosts.blocklist. Therefore, we need to create this list and add entries.

Make list
```
sudo nano /etc/hosts.blocklist
```

Add entries:
```
0.0.0.0 ads.example.com
0.0.0.0 tracker.example.net
```

Once the blocklist is set, restart the dnsmasq service to apply changes:

```
sudo systemctl restart dnsmasq
```

And to enable dnsmasq on boot:

```
sudo systemctl enable dnsmasq
```

#### 4. Test the Pi as a DNS Server

Now to test to see if the DNS server is functional.

On linux OS devices, we can set the DNS server to use in the /etc/resolv.conf file. So we will go to this file to point the pi to itself first to test the DNS services.

```
sudo nano /etc/resolv.conf
```

Replace all lines with:

```
nameserver 127.0.0.1
```

Now that this is setup, we can test to see if the DNS server is resolving domains correctly. I will use the dig command to get the IP address for google.com and verify that the DNS service is functional:

```
jonah@raspberrypi:/etc $ dig google.com

; <<>> DiG 9.18.28-1~deb12u2-Debian <<>> google.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 53048
;; flags: qr rd ra; QUERY: 1, ANSWER: 6, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;google.com.                    IN      A

;; ANSWER SECTION:
google.com.             135     IN      A       142.251.185.102
google.com.             135     IN      A       142.251.185.101
google.com.             135     IN      A       142.251.185.139
google.com.             135     IN      A       142.251.185.100
google.com.             135     IN      A       142.251.185.138
google.com.             135     IN      A       142.251.185.113

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Wed Jan 01 08:38:59 EST 2025
;; MSG SIZE  rcvd: 135
```

From the above results, we see the line ";; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)" which means that the dnsmasq service we just setup was used. And when we test the IP address results in "ANSWER SECTION:" we are successfully navigated to google.com.

Now let's test the blocklist:

```
jonah@raspberrypi:/etc $ dig ads.example.com

; <<>> DiG 9.18.28-1~deb12u2-Debian <<>> ads.example.com
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 51259
;; flags: qr aa rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;ads.example.com.               IN      A

;; ANSWER SECTION:
ads.example.com.        0       IN      A       0.0.0.0

;; Query time: 0 msec
;; SERVER: 127.0.0.1#53(127.0.0.1) (UDP)
;; WHEN: Wed Jan 01 08:42:34 EST 2025
;; MSG SIZE  rcvd: 60
```

Perfect! The unwanted domain name "ads.example.com" is sent to the black hole 0.0.0.0.

To double check the DNS services, we can view the logging for dnsmasq:

```
jonah@raspberrypi:/etc $ journalctl -ru dnsmasq.service
Jan 01 08:42:34 raspberrypi dnsmasq[603]: 4 127.0.0.1/57280 /etc/hosts.blocklist ads.example.com is 0.0.0.0
Jan 01 08:42:34 raspberrypi dnsmasq[603]: 4 127.0.0.1/57280 query[A] ads.example.com from 127.0.0.1
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 cached google.com is 142.251.185.113
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 cached google.com is 142.251.185.138
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 cached google.com is 142.251.185.100
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 cached google.com is 142.251.185.139
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 cached google.com is 142.251.185.101
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 cached google.com is 142.251.185.102
Jan 01 08:38:59 raspberrypi dnsmasq[603]: 3 127.0.0.1/58894 query[A] google.com from 127.0.0.1
```

The above shows the DNS server side of things when we requested google.com and ads.example.com, success! Note: I am using the raspberry pi OS which does not have the traditional linux logging, instead logs are found using the journalctl command.

I will also test from another device on the same LAN. To do this, first change your DNS server settings on your test device to the IP of the Pi. Next, simply go to google.com like you normally would and this should work fine:

![image](https://github.com/user-attachments/assets/7b4aaa43-d2df-48ae-937c-2d36bd35a383)

Now, see if the blocking capabilities are working by going to any entry in your blocklist:

![image](https://github.com/user-attachments/assets/f8c1dbf4-561f-4703-a951-a960dce8212a)

Looks good, we can now check the Raspberry Pi's logs to verify. You should see the following lines included in the journal:

```
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 reply www3.l.google.com is NODATA
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 reply ogs.google.com is <CNAME>
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 forwarded ogs.google.com to 8.8.8.8
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 forwarded ogs.google.com to 1.1.1.1
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 forwarded ogs.google.com to 8.8.8.8
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 forwarded ogs.google.com to 1.1.1.1
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 cached ogs.google.com is <CNAME>
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 107 192.168.1.122/62735 query[HTTPS] ogs.google.com from 192.168.1.122
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached www3.l.google.com is 142.251.165.139
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached www3.l.google.com is 142.251.165.113
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached www3.l.google.com is 142.251.165.100
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached www3.l.google.com is 142.251.165.102
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached www3.l.google.com is 142.251.165.138
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached www3.l.google.com is 142.251.165.101
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 cached ogs.google.com is <CNAME>
Jan 01 09:06:52 raspberrypi dnsmasq[603]: 106 192.168.1.122/54495 query[A] ogs.google.com from 192.168.1.122
```

```
Jan 01 09:05:11 raspberrypi dnsmasq[603]: 87 192.168.1.122/62864 /etc/hosts.blocklist ads.example.com is 0.0.0.0
```

Above, the 192.168.1.122 device is my testing device, you should see the IP address of the device you are testing with. Other than that, everything is working as desired.

## Additional Functionality

The above was just the base DNS service - the tip of the iceberg!

Some other customizations include:
- automating blocklist updates, using third-party comprehensive list
- monitoring traffic trends
- formatting dns resolution data into a user friendly GUI with charts, descriptors, etc - similar to PiHole capabilities.
- DNSSEC for added security 
