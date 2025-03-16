# HTB Proxy - HTB CTF WEB 1000

Your team is tasked to penetrate the internal networks of a raider base in order to acquire explosives, scanning their ip ranges revealed only one alive host running their own custom implementation of an HTTP proxy, have you got enough wit to get the job done?

## Overall Solution

Server is behind proxy at the address provided. Find server destination with /server-status endpoint. Access backend server. RCE for flag

## Proxy & Backend Server

Looking at index.js, there is an express.js application running on port 5000. This is where we want to hit the /flushinterface endpoint which has a RCE vuln (ip-wrapper documentation)

There is a check for "flushinterface" in the main.go file:

```
	if strings.Contains(strings.ToLower(request.URL), string([]byte{102, 108, 117, 115, 104, 105, 110, 116, 101, 114, 102, 97, 99, 101})) {
		var responseText string = badReqResponse("Not Allowed")
		frontendConn.Write([]byte(responseText))
		frontendConn.Close()
		return
	}
```


get server status

```
	if request.URL == string([]byte{47, 115, 101, 114, 118, 101, 114, 45, 115, 116, 97, 116, 117, 115}) {
		var serverInfo string = GetServerInfo()
		var responseText string = okResponse(serverInfo)
		frontendConn.Write([]byte(responseText))
		frontendConn.Close()
		return
	}

```

endpoint of /server-status gives

```Hostname: ng-team-219485-webhtbproxybiz2024-9z6ac-55594c555c-znxmw, Operating System: linux, Architecture: amd64, CPU Count: 4, Go Version: go1.21.10, IPs: 192.168.67.133```

The burp request below interacts with the server behind the proxy:

![accessserver](https://github.com/user-attachments/assets/8ac0d119-e754-4094-9f08-2e8149f28422)


Sending a POST to the /getAddresses proves that we are able to interact with the backend server:

![getaddresses](https://github.com/user-attachments/assets/9aac7106-22c4-4c9b-930d-a94448779504)

Now we need to figure out how to use /flushinterface to solve the challenge

## Request Smuggling

/flushinterface is blocked when trying to go through the proxy:

```
	if strings.Contains(strings.ToLower(request.URL), string([]byte{102, 108, 117, 115, 104, 105, 110, 116, 101, 114, 102, 97, 99, 101})) {
		var responseText string = badReqResponse("Not Allowed")
		frontendConn.Write([]byte(responseText))
		frontendConn.Close()
		return
	}
```

To bypass this, we want the server to make the request rather than the proxy. This is request smuggling.

Payload and response for to exploit the proxies double newline separation vulnerability.

![flush1](https://github.com/user-attachments/assets/316d8f26-9229-48cd-8ab8-edc6f75b4b49)


## IP-Wrapper

ip-wrapper is similar to linux command and calling ip.addr.flush() should remove all assign IP addresses from a given network interface.

Code for the flush function is vulnerable to RCE due to the 'exec':

```
function flush(interfaceName) {
    return new Promise((resolve, reject) => {
        exec(`ip address flush dev ${interfaceName}`, (error, stdout, stderr) => {
            if (stderr) {
                if(stderr.includes('Cannot find device')) {
                    reject(new Error('Cannot find device ' + interfaceName));
                } else {
                    reject(new Error('Error flushing IP addresses: ' + stderr));
                }
                return;
            }

            resolve();
        });
    });
}
```

Testing RCE (blind so need to update something we can access -> index.html)

payload:

![rcepaytest](https://github.com/user-attachments/assets/cd0fafcb-e81a-4aa1-9662-7df033786ad2)


result:

![rcetestres](https://github.com/user-attachments/assets/2c9aa01a-737f-4a46-9f61-5699fbd6f64b)


After trying various payloads to find the flag, the validateInput() function removes whitespaces from the interface. To bypass this, use ${IFS} instead of whitespace for the final payload:

```{"interface":";cat${IFS}/flag.txt>/app/proxy/includes/index.html;"}```

This displays the flag on the index.html page for the proxy!

## Learning / Resources

- web proxies
- curl -x
- ip-wrapper
	- https://github.com/AlchemillaHQ/ip-wrapper/blob/master/src/addresses.js
- request smuggling
	- https://portswigger.net/web-security/request-smuggling
- nip io
