#!/bin/sh

cyan='\033[0;36m'
red='\033[0;31m'
ylw='\033[0;33m'
nc='\033[0m'

read -p "site or ip:  " site

echo Beginning recon for $cyan$site$nc

# WHOIS
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo $ylw"\nWHOIS\n\n"$nc 
whois $site | grep -i 'Domain\|Registrant\|Created\|Registrar\|Registry\|Updated\|Creation\|Server\|DNSSEC\|Admin\|Tech' | grep -v 'Terms of Use:'
echo '\n'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# dig
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo $ylw"\nDIG\n\n"$nc 
dig $site
echo '\n'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# dig
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo $ylw"\nWHATWEB\n\n"$nc 
whatweb $site
echo '\n'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# NMAP
echo +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
echo $ylw"\nNMAP\n\n"$nc 
nmap -oN /dev/null -sCV -p 80,443,8080 $site
echo '\n'+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


