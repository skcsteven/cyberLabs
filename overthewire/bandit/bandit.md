
0 -> 1

simple read file
ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If

1 -> 2

handle file name '-'

bandit1@bandit:~$ cat /home/bandit1/-
263JGJPfgU6LtdEvgfWU1XP5yac29mFx

2 -> 3

how to handle filenames with spaces
bandit2@bandit:~$ cat "spaces in this filename"
MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx

3->4

how to show hidden files, use -a switch for ls command
bandit3@bandit:~/inhere$ ls -la
total 12
drwxr-xr-x 2 root    root    4096 Sep 19 07:08 .
drwxr-xr-x 3 root    root    4096 Sep 19 07:08 ..
-rw-r----- 1 bandit4 bandit3   33 Sep 19 07:08 ...Hiding-From-You
bandit3@bandit:~/inhere$ cat ...Hiding-From-You
2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ

4 -> 5

get human readable files

bandit4@bandit:~/inhere$ find /home/bandit4/inhere -type f -exec file {} \; | grep -i 'text'
/home/bandit4/inhere/-file07: ASCII text
bandit4@bandit:~/inhere$ cat /home/bandit4/inhere/-file07
4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw

---or could use wildcard operator

bandit4@bandit:~/inhere$ file ./*
./-file00: data
./-file01: data
./-file02: data
./-file03: data
./-file04: data
./-file05: data
./-file06: data
./-file07: ASCII text
./-file08: data
./-file09: data

5 ->6

find file with multiple filters: readable, 1033 bytes, not executable

bandit5@bandit:~/inhere$ find /home/bandit5/inhere -type f -size 1033c -exec file {} \; | grep 'ASCII'
/home/bandit5/inhere/maybehere07/.file2: ASCII text, with very long lines (1000)
bandit5@bandit:~/inhere$ cat /home/bandit5/inhere/maybehere07/.file2
HWasnPhtq9AVKe0dmk45nxy20cvUa6EG

6 -> 7


find file based on: user owner, group owner, size
bandit6@bandit:/$ find /  -user bandit7 -group bandit6 -size 33c 2> /dev/null 
bandit6@bandit:/$ cat /var/lib/dpkg/info/bandit7.password
morbNTDkSW6jIlUc0ymOdMaLnOlFVAaj

2> /dev/null uses bash redirection to throw away error messages


7 -> 8


bandit7@bandit:~$ cat data.txt | grep 'millionth'
millionth       dfwvzFQi4mU0wfNbFOe9RoWskMLg7eEc


8 -> 9

get line of text that only occurs once
bandit8@bandit:~$ sort  data.txt | uniq -u
4CKMh1JI91bUIZZPXDqGanal4xvAg0JM


9 -> 10

get human-readable strings from file and containing several '=' characters
bandit9@bandit:~$ strings data.txt | grep ===
}========== the
3JprD========== passwordi
~fDV3========== is
D9========== FGUW5ilLVJrxX9kMYMmlN4MgbpfMiqey


10 -> 11

decode base64 encryption
bandit10@bandit:~$ base64 --decode data.txt
The password is dtR173fZKb0RRsDFSGsg2RWnpNVj3qRr

11 -> 12


using tr for rot13 decryption
bandit11@bandit:~$ cat data.txt | tr 'A-Za-z' 'N-ZA-Mn-za-m'
The password is 7x16WNeHIi5YkIhWsfFIqoognUTyj9Q4


12 -> 13

using tar, bunzip, gunzip, and renaming files. mktemp -d
FO5dwFsc0cbaIiH0h8J2eUks2vdTDwAn


13 -> 14

ssh using private key, get private key from bandit13, copy paste to local server
┌──(kali㉿kali)-[~/Desktop]
└─$ chmod 600 sshkey.private  #private keys should not be availble to anyone
                                                                                                                    
┌──(kali㉿kali)-[~/Desktop]
└─$ ssh bandit.labs.overthewire.org -p2220 -l bandit14 -i sshkey.private

14 -> 15


bandit14@bandit:/etc/bandit_pass$ cat bandit14
MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS

bandit14@bandit:/etc/bandit_pass$ echo MU4VWeTyJk8ROof1qqmcBPaLh7lDCPvS | nc localhost 30000
Correct!
8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo

15 -> 16

using ssl/tls encryption to send data
bandit15@bandit:~$ cat /etc/bandit_pass/bandit15
8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo

bandit15@bandit:~$ openssl s_client localhost:30001
------ connection details will show up, enter the passwrod for bandit 15----
8xCjnmgoKbGLhHFAZlGE5Tmu4M2tKJQo
Correct!
kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx


16 -> 17

find open port between 31000-32000 with SSL/TLS, send current password

bandit16@bandit:/tmp/tmp.PVxutX6GxW$ nmap -script ssl-enum-ciphers localhost -p31000-32000
Starting Nmap 7.94SVN ( https://nmap.org ) at 2024-12-29 01:49 UTC
Nmap scan report for localhost (127.0.0.1)
Host is up (0.00047s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT      STATE SERVICE
31046/tcp open  unknown
31518/tcp open  unknown
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (secp256r1) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_CCM (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_CCM_8 (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CCM (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CCM_8 (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 4096) - A
|       TLS_RSA_WITH_ARIA_128_GCM_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_ARIA_256_GCM_SHA384 (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256 (rsa 4096) - A
|     compressors: 
|       NULL
|     cipher preference: client
|     warnings: 
|       Key exchange (secp256r1) of lower strength than certificate key
|   TLSv1.3: 
|     ciphers: 
|       TLS_AKE_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_AKE_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|     cipher preference: client
|_  least strength: A
31691/tcp open  unknown
31790/tcp open  unknown
| ssl-enum-ciphers: 
|   TLSv1.2: 
|     ciphers: 
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_128_GCM_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_ARIA_256_GCM_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_128_CBC_SHA256 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CAMELLIA_256_CBC_SHA384 (secp256r1) - A
|       TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305_SHA256 (secp256r1) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_CCM (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_CCM_8 (rsa 4096) - A
|       TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CCM (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_CCM_8 (rsa 4096) - A
|       TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 4096) - A
|       TLS_RSA_WITH_ARIA_128_GCM_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_ARIA_256_GCM_SHA384 (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_128_CBC_SHA256 (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 4096) - A
|       TLS_RSA_WITH_CAMELLIA_256_CBC_SHA256 (rsa 4096) - A
|     compressors: 
|       NULL
|     cipher preference: client
|     warnings: 
|       Key exchange (secp256r1) of lower strength than certificate key
|   TLSv1.3: 
|     ciphers: 
|       TLS_AKE_WITH_AES_128_GCM_SHA256 (ecdh_x25519) - A
|       TLS_AKE_WITH_AES_256_GCM_SHA384 (ecdh_x25519) - A
|       TLS_AKE_WITH_CHACHA20_POLY1305_SHA256 (ecdh_x25519) - A
|     cipher preference: client
|_  least strength: A
31960/tcp open  unknown

Nmap done: 1 IP address (1 host up) scanned in 0.75 seconds


bandit16@bandit:/tmp/tmp.PVxutX6GxW$ openssl s_client -quiet -connect localhost:31790
Can't use SSL_get_servername
depth=0 CN = SnakeOil
verify error:num=18:self-signed certificate
verify return:1
depth=0 CN = SnakeOil
verify return:1
kSkvUpMQ7lBYyCM4GBPvCvT1BfWRy0Dx
Correct!
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAvmOkuifmMg6HL2YPIOjon6iWfbp7c3jx34YkYWqUH57SUdyJ
imZzeyGC0gtZPGujUSxiJSWI/oTqexh+cAMTSMlOJf7+BrJObArnxd9Y7YT2bRPQ
Ja6Lzb558YW3FZl87ORiO+rW4LCDCNd2lUvLE/GL2GWyuKN0K5iCd5TbtJzEkQTu
DSt2mcNn4rhAL+JFr56o4T6z8WWAW18BR6yGrMq7Q/kALHYW3OekePQAzL0VUYbW
JGTi65CxbCnzc/w4+mqQyvmzpWtMAzJTzAzQxNbkR2MBGySxDLrjg0LWN6sK7wNX
x0YVztz/zbIkPjfkU1jHS+9EbVNj+D1XFOJuaQIDAQABAoIBABagpxpM1aoLWfvD
KHcj10nqcoBc4oE11aFYQwik7xfW+24pRNuDE6SFthOar69jp5RlLwD1NhPx3iBl
J9nOM8OJ0VToum43UOS8YxF8WwhXriYGnc1sskbwpXOUDc9uX4+UESzH22P29ovd
d8WErY0gPxun8pbJLmxkAtWNhpMvfe0050vk9TL5wqbu9AlbssgTcCXkMQnPw9nC
YNN6DDP2lbcBrvgT9YCNL6C+ZKufD52yOQ9qOkwFTEQpjtF4uNtJom+asvlpmS8A
vLY9r60wYSvmZhNqBUrj7lyCtXMIu1kkd4w7F77k+DjHoAXyxcUp1DGL51sOmama
+TOWWgECgYEA8JtPxP0GRJ+IQkX262jM3dEIkza8ky5moIwUqYdsx0NxHgRRhORT
8c8hAuRBb2G82so8vUHk/fur85OEfc9TncnCY2crpoqsghifKLxrLgtT+qDpfZnx
SatLdt8GfQ85yA7hnWWJ2MxF3NaeSDm75Lsm+tBbAiyc9P2jGRNtMSkCgYEAypHd
HCctNi/FwjulhttFx/rHYKhLidZDFYeiE/v45bN4yFm8x7R/b0iE7KaszX+Exdvt
SghaTdcG0Knyw1bpJVyusavPzpaJMjdJ6tcFhVAbAjm7enCIvGCSx+X3l5SiWg0A
R57hJglezIiVjv3aGwHwvlZvtszK6zV6oXFAu0ECgYAbjo46T4hyP5tJi93V5HDi
Ttiek7xRVxUl+iU7rWkGAXFpMLFteQEsRr7PJ/lemmEY5eTDAFMLy9FL2m9oQWCg
R8VdwSk8r9FGLS+9aKcV5PI/WEKlwgXinB3OhYimtiG2Cg5JCqIZFHxD6MjEGOiu
L8ktHMPvodBwNsSBULpG0QKBgBAplTfC1HOnWiMGOU3KPwYWt0O6CdTkmJOmL8Ni
blh9elyZ9FsGxsgtRBXRsqXuz7wtsQAgLHxbdLq/ZJQ7YfzOKU4ZxEnabvXnvWkU
YOdjHdSOoKvDQNWu6ucyLRAWFuISeXw9a/9p7ftpxm0TSgyvmfLF2MIAEwyzRqaM
77pBAoGAMmjmIJdjp+Ez8duyn3ieo36yrttF5NSsJLAbxFpdlc1gvtGCWW+9Cq0b
dxviW8+TFVEBl1O4f7HVm6EpTscdDxU+bCXWkfjuRb7Dy9GOtt9JPsX8MBTakzh3
vBgsyi/sN3RqRBcGU40fOoZyfAMT8s1m/uYv52O6IgeuZ/ujbjY=
-----END RSA PRIVATE KEY-----


after logged in to 17, get pass:
EReVavePLFHtFlFsjn3hyzMlvSuSAcRD

17 -> 18

bandit17@bandit:~$ diff -y passwords.new passwords.old | grep '|'
x2gLTTjFwMOhQ8oWNbMN362QKxfRqGlO                              | ktfgBvpMzWKR5ENj26IbLGSblgUG9CzB


18 -> 19

┌──(kali㉿kali)-[~/Desktop]
└─$ echo ls | ssh bandit.labs.overthewire.org -p2220 -l bandit18 
Pseudo-terminal will not be allocated because stdin is not a terminal.
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: 
readme

┌──(kali㉿kali)-[~/Desktop]
└─$ echo cat readme | ssh bandit.labs.overthewire.org -p2220 -l bandit18 
Pseudo-terminal will not be allocated because stdin is not a terminal.
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit18@bandit.labs.overthewire.org's password: 
cGWpMaKXVwDUNgPAVJbWYuGHVn9zl3j8

19 -> 20

bandit19@bandit:~$ ./bandit20-do whoami
bandit20
bandit19@bandit:~$ ./bandit20-do cat /etc/bandit_pass/bandit20
0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO


20 -> 21

--------- listener -----
bandit20@bandit:~$ nc -l -p 4444
0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO
EeoULMCra2q0dSkYj561DX7s1CpBuOBt

--------server-------
bandit20@bandit:~$ ./suconnect 4444
Read: 0qXahG8ZjOVMN9Ghs7iOWsCfZyXOUbYO
Password matches, sending next password

21 -> 22

bandit21@bandit:/usr/bin$ file cronjob_bandit22.sh
cronjob_bandit22.sh: Bourne-Again shell script, ASCII text executable
bandit21@bandit:/usr/bin$ ./cronjob_bandit22.sh
chmod: changing permissions of '/tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv': Operation not permitted
./cronjob_bandit22.sh: line 3: /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv: Permission denied
bandit21@bandit:/usr/bin$ cat ./cronjob_bandit22.sh
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv

bandit21@bandit:/tmp/tmp.1CV2u5cQQd$ cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
tRae0UfB9v0UzbCdn9cY0gQnds9GF58Q

22 -> 23

bandit22@bandit:/etc/cron.d$ cat cronjob_bandit23
@reboot bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null
* * * * * bandit23 /usr/bin/cronjob_bandit23.sh  &> /dev/null

bandit22@bandit:/usr/bin$ cat cronjob_bandit23.sh

'''
#!/bin/bash
myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"
cat /etc/bandit_pass/$myname > /tmp/$mytarget
'''

make copy of file and change myname to bandit23 to find out the name of the tmp file that is storing the password file:

```
#!/bin/bash
myname='bandit23'
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)
echo $mytarget
```

bandit22@bandit:/tmp/tmp.8hA90VK4xg$ ./copy.sh
8ca319486bfbbc3663ea0fbe81326349
bandit22@bandit:/tmp/tmp.8hA90VK4xg$ cat /tmp/8ca319486bfbbc3663ea0fbe81326349
0Zf11ioIjMVN551jX3CmStKLYqjk54Ga

23 -> 24


cronjob runs and deletes files every minute in /var/spool/bandit24/foo so we have to leave a shell script that will read the bandit24 password, output it to a file that we can read. Essentially this method allows us to read /etc/bandit_pass/bandit24 as bandit 23.

```
#!/bin/bash

cat /etc/bandit_pass/bandit24 > /tmp/tmp.05RdosA5B0

```
gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8

24 -> 25

A daemon is listening on port 30002 and will give you the password for bandit25 if given the password for bandit24 and a secret numeric 4-digit pincode. There is no way to retrieve the pincode except by going through all of the 10000 combinations, called brute-forcing.

brute force script
```
#!/bin/bash

password="gb8KRRCsshuZXI0tUuR6ypOFjiZbf3G8"

for i in {1..9999} 
do
   echo "$password $i"
done
```

result:

bandit24@bandit:/tmp/tmp.QVCQmkAiwV$ ./brute.sh | nc localhost 30002 | grep bandit25
I am the pincode checker for user bandit25. Please enter the password for user bandit24 and the secret pincode on a single line, separated by a space.
The password of user bandit25 is iCi86ttT4KSNe1armKiwbQNmB3YJP3q4

25 -> 26

Logging in to bandit26 from bandit25 should be fairly easy… The shell for user bandit26 is not /bin/bash, but something else. Find out what it is, how it works and how to break out of it.

/etc/passwd - Tracks registered users and their basic attributes, such as their username, user ID, group ID, home directory, and default shell

bandit25@bandit:/etc$ cat passwd | grep bandit26
bandit26:x:11026:11026:bandit level 26:/home/bandit26:/usr/bin/showtext

bandit25@bandit:/etc$ cat /usr/bin/showtext

```
#!/bin/sh

export TERM=linux

exec more ~/text.txt
exit 0
```

https://mayadevbe.me/posts/overthewire/bandit/level26/

s0773xxkk0MXfdqOfPRVr9L3jJBUOgCZ

26 -> 27

bandit26@bandit:~$ ./bandit27-do cat /etc/bandit_pass/bandit27
upsNCc7vzaRDx6oZC6GiR6ERwe1MowGB

27 -> 28

bandit27@bandit:~$ mktemp -d
/tmp/tmp.DxgM7gaJ7Z
bandit27@bandit:/tmp/tmp.DxgM7gaJ7Z$ git clone ssh://bandit27-git@localhost:2220/home/bandit27-git/repo
Yz9IpL0sBcCeuG7m9uQFt8ZNpS4HZRcN

28 -> 29

First clone repo same way as 27 -> 28

README.md:

# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx

View previous versions of the README.md file:

```
git log -p README.md
```

4pT1t5DENaYuqnqvadYs1oE4QLCdjmJ7

29 -> 30

```
bandit29@bandit:/tmp/tmp.V7Pix9hCsC/repo$ git log --all
commit 6ac7796430c0f39290a0e29a4d32e5126544b022 (HEAD -> master, origin/master, origin/HEAD, README.md)
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Sep 19 07:08:41 2024 +0000

    fix username

commit 081ac380883f49b0d9dc76a82c53211ef7ba74b0 (origin/dev)
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Sep 19 07:08:41 2024 +0000

    add data needed for development

commit 72267325ede0966e2b002e11154e6a867ebdd5b4 (origin/sploits-dev)
Author: Morla Porla <morla@overthewire.org>
Date:   Thu Sep 19 07:08:41 2024 +0000

    add some silly exploit, just for shit and giggles

commit e65a928cca4db1863b478cf5e93d1d5b1c1bd6b2
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Sep 19 07:08:41 2024 +0000

    initial commit of README.md

commit 03aa12c85ea4c1ea170b8e5fe80e55de7853b4db
Author: Ben Dover <noone@overthewire.org>
Date:   Thu Sep 19 07:08:41 2024 +0000

    add gif2ascii
    
bandit29@bandit:/tmp/tmp.V7Pix9hCsC/repo$ git show 081ac380883f49b0d9dc76a82c53211ef7ba74b0
```

qp30ex3VLz5MDG1n91YowTv4Q8l7CDZL


30 -> 31

Show tags

```
git tag -l
```

Read tag

```
git show <tag_name>
```

fb5S2xb7bRyFmAvQYQGEqsbhVyJqhnDy


31 -> 32

First change .gitignore to allow .txt files then add/commit/push file:

```
bandit31@bandit:/tmp/tmp.LvFcDSSZsq/repo$ nano .gitignore
Unable to create directory /home/bandit31/.local/share/nano/: No such file or directory
It is required for saving/loading search history or cursor positions.

bandit31@bandit:/tmp/tmp.LvFcDSSZsq/repo$ git add key.txt
bandit31@bandit:/tmp/tmp.LvFcDSSZsq/repo$ git commit -m 'new'
[master 8d14dfe] new
 1 file changed, 1 insertion(+)
 create mode 100644 key.txt
bandit31@bandit:/tmp/tmp.LvFcDSSZsq/repo$ git push origin master
The authenticity of host '[localhost]:2220 ([127.0.0.1]:2220)' can't be established.
ED25519 key fingerprint is SHA256:C2ihUBV7ihnV1wUXRb4RrEcLfXC5CXlhmAAM/urerLY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Could not create directory '/home/bandit31/.ssh' (Permission denied).
Failed to add the host to the list of known hosts (/home/bandit31/.ssh/known_hosts).
                         _                     _ _ _   
                        | |__   __ _ _ __   __| (_) |_ 
                        | '_ \ / _` | '_ \ / _` | | __|
                        | |_) | (_| | | | | (_| | | |_ 
                        |_.__/ \__,_|_| |_|\__,_|_|\__|
                                                       

                      This is an OverTheWire game server. 
            More information on http://www.overthewire.org/wargames

bandit31-git@localhost's password: 
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 2 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 318 bytes | 318.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
remote: ### Attempting to validate files... ####
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
remote: Well done! Here is the password for the next level:
remote: 3O9RfhqyAlVBEZpVb6LYStshZoqoSx5K 
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
To ssh://localhost:2220/home/bandit31-git/repo
 ! [remote rejected] master -> master (pre-receive hook declined)
error: failed to push some refs to 'ssh://localhost:2220/home/bandit31-git/repo'

```

32 -> 33

$0 escapes the uppercase pain

tQdtbs5D5i2vJwkO8mEyYEyTL8izoeJ0


ALL DONE !!!
