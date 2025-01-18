## Cody's First Blog - Hacker101 CTF - Web (moderate)

#### Initial recon / First flag

The initial load point is a simple blog:



So the blog seems to be making use of PHP. I will just test a simple XSS injection for the comments section:

```
<?php echo "Hello world"; ?>
```

And this gives us our first flag!



Using devtools, there is an interesting comment that shows that the admin login page can be accessed by adding the following to the URL:

```
?page=admin.auth.inc
```

When performing a quick check of the ?page parameter, I enter a value of "0" to see what happens. An interesting error message comes up:




The error messages show that the page= parameter searches the server for the supplied input/page with a .php extension using the include() function. This is a Local File Inclusion (LFI) vulnerability and could come in handy later.


I will use dirb to see what other subdirectories/pages I can find:

```
dirb https://43e9ea0719c936aa934064f61e7eba02.ctf.hacker101.com/ -w /usr/share/wordlists/dirb/big.txt
```

The results of this tell us that we can view the php.ini (php configuration file) and a /posts/ directory.

#### Exploring enumerated attack vectors

Our current vectors:

1. the admin page that might be susceptible to injection vulnerabilities
2. the comment box which we know doesn't sanitize too well
3. the error messages that are displayed from the ?page= parameter which indicate an LFI through the include() method

Testing various values for the page parameter, when I use page=index, I get an error message:

```
Fatal error: Allowed memory size of 134217728 bytes exhausted (tried to allocate 16384 bytes) in /app/index.php on line 20
```

This could signify a buffer overflow vulnerability. The code takes the page value and runs it through the include() method to find that file and read the contents of it to line 20 in "/app/index". So this error tells me exactly how many bytes are allowed in the buffer for the input on line 20.

OK... ignore the buffer overflow path, the reason why the fatal error occurs is because I am pretty much telling the index.php file to load itself by entering "index" for the include() method - this creates a recursive loop.

#### admin page

While testing common files for PHP and web apps for the ?page= parameter, I learn that the include() method automatically appends .php to the input and that this can be escaped with a null byte "%00" (this shouldn't work because of the PHP version but for this CTF it does).

Also, when looking at the provided comment in devtools for the admin.auth.inc page, I research more into the .inc extension and learn that it is used for PHP apps to indicate that a file contains code meant to be included in other PHP files using the include() method. So in other words, if I know a web app is using include() its a good idea to also test the .inc extension tagged on.

With this knowledge, I try ?page=admin.inc to see if this will get me anywhere... and it leads me straight to the admin page --- bypassing the authentication requirement and granting the second flag:




#### Revisiting the comment functionality

So we already know that the comment box is susceptible to php code injection, but earlier we had to wait for the comment to be approved by an admin for it to persist on the blog page. With admin access, I will see if I can perform a persistent XSS

For the comment, my payload is:

```
<?php echo shell_exec('ls -la'); ?>
```

I approve this comment and go back to the page but the results of the command do not show up, only the empty comment is on page by inspecting dev tools.

After trying a variety of payloads thinking that my PHP was off, I research new methods. So far using the ?page= parameter with the include() method has only been targetted at files. But if I try sending http://localhost/<PAGE WITH COMMENTS>, the web app loads the index file with all the PHP comments loaded in. So when the page loads, the php comments are also run and their results are displayed on the page.

From here, I just enumerate the system to find the final flag:

(long story short, I learned the magic of grep)

```
<?php echo shell_exec('grep -R FLAG'); ?>
```
