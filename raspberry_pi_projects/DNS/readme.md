# Raspberry Pi DNS Server

In this home lab, I set up my own DNS server with a Rapsberry Pi model 3B to learn practical networking skills. My Pi is connected via ethernet directly to my home router and I perform all configurations headless by SSHing into the pi from another device. I will make use of DNSMASQ on my Pi to provide DNS services.

## Steps

1. Set up static IP address on Raspberry Pi

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

2. Install and Configure dnsmasq

3. Create a Blocklist

4. Test the Pi as a DNS Server
