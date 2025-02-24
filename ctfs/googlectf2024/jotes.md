# JOTES - googlectf - web

Welcome to our note taking app, I hope you can't see what we're writing

https://jwt-notes-web.2024-bq.ctfcompetition.com/


With the url provided and name of the challenge, we will likely be exploiting the JWT cookie authentication process.

After exploring the site, it seems to be a note taking application for users. To solve this challenge I first created two accounts "falcon" and "jim".

Once logged in to these accounts, they are given a JWT. I decode these using jwt.io:

---


---

After researching JWT vulnerabilities, I try the none encoding exploit. This exploit relies on setting the hash "alg" value in the header to "none", thereby bypassing the signature portion of JWT.

JWT headers and payloads are encrypted using base64 so I first test to see if the none encoding exploit is able by trying to view "jim"s notes from the falcon account by changing my token.

For the header portion of the JWT:

__eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0__

And then the payload, I need to encode the following to base64: (I know the id for jim is 16 by looking at his token) 

__{"user_id":16,"role":"user","username":"jim"}__

Linux commands:

__echo '{"user_id":16,"role":"user","username":"jim"}' >> data.txt__

__base64 data.txt__

After appending the encoded payload to the header, __I made sure to not forget a trailing dot in place of the signature__

After updating the application cookies, I was able to view jim's notes!

To get the flag here I just had to modify the payload portion of the none encoding JWT to {"user_id":1,"role":"admin","username":"admin"} where I know that the user "admin" exists from an error message at the register endpoint when I tried to create an admin account.

The resulting JWT:

__eyJ0eXAiOiJKV1QiLCJhbGciOiJub25lIn0.eyJ1c2VyX2lkIjoxLCJyb2xlIjoiYWRtaW4iLCJ1c2VybmFtZSI6ImFkbWluIn0K.__

--


# Learning/Sources

- Real world IDOR JWT exploit - https://medium.com/@AlQa3Qa3_M0X0101/how-i-was-able-to-get-account-takeover-via-idor-form-jwt-caaf7ea58aa 
- JWT none encoding - https://blog.pentesteracademy.com/hacking-jwt-tokens-the-none-algorithm-67c14bb15771
