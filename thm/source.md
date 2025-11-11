# source - easy

### Recon with NMAP

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 b7:4c:d0:bd:e2:7b:1b:15:72:27:64:56:29:15:ea:23 (RSA)
|   256 b7:85:23:11:4f:44:fa:22:00:8e:40:77:5e:cf:28:7c (ECDSA)
|_  256 a9:fe:4b:82:bf:89:34:59:36:5b:ec:da:c2:d3:95:ce (ED25519)
10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
|_http-trane-info: Problem with XML parsing of /evox/about
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

The vulnerable service is Webmin with MiniServ 1.890. A quick google search shows us that there is a reverse shell exploit based off of a XSS on the password_change.cgi endpoint (https://www.cve.org/CVERecord?id=CVE-2019-15107)

### Solution

I'll first try to see the password_change.cgi endpoint and see what happens. Interesting, the safety page leaks security information to us attackers - ironic:

<img width="451" height="636" alt="Screenshot 2025-11-08 at 18-33-50 Security Warning" src="https://github.com/user-attachments/assets/1ecaa71c-9e9d-4031-aeca-99a9c42360fa" />


Continuing the CVE search, I found a script to RCE the machine:

https://github.com/n0obit4/Webmin_1.890-POC

I use this RCE to find the root.txt flag by enumerating the system and finding the flag in the ~ directory.

Next I find the user.txt flag by enumerating users and navigating to "dark"s account.
