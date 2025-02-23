# Doors Every (Part I) - google ctf - web

A security update about profiles? There's no way there could be a flag there. Unless?

https://secuweb-web.2024-bq.ctfcompetition.com/

![home](https://github.com/user-attachments/assets/e56b783c-3d2f-4385-aab0-e937381b852f)


Theres a login page

![login](https://github.com/user-attachments/assets/f6deaa24-03d7-48a3-b47f-d267dedd14b2)



First I login to the guest account to check out the page. It seems to be a simple blog.

There are some interesting (useless) blog posts, a profile page, and a secret message function that is locked for the guest account.

The solution lies in a hint on the home page of guest:

![secUpdate](https://github.com/user-attachments/assets/60fa6f73-9743-4c1d-92a6-221f7617b2a7)


After this I go to the profile page for guest and notice that it is at the /profile/guest endpoint, I test /profile/admin and there the flag is!

# Doors Every (Part II) - google ctf - web

There are a few news articles there, but there's something odd about their URLs...

The news articles all have the /news/1 or some other number for their location. However there is a gap between 5 and 7 so visiting 6 gives us the flag.

# Doors Every (Part III) - google ctf - web

There are a few news articles there, but there's something odd about their URLs...

Secret messages! Probably the most secure part of this website. There's no way to guess those URLs. ...Unless?

Looking around we find the endpoint /message/<SHA256_HASH>, where the hash value is the hash of integers like 1-100. To capture the flag I first create a script to generate the hashes for 1-1000 and then send them to burp intruder to test. One file gave a hint that the index to look at was Douglas Adam's favorite number so visiting the hash of such number presented the flag.

```
#!/bin/bash

# Output file
output_file="sha3_hashes.txt"

# Loop through numbers 1 to 1000
for i in {1..1000}
do
    # Compute SHA3-256 hash using sha3sum, and remove any trailing hyphen
    hash=$(printf "%s" "$i" | sha3sum -a 256| awk '{print $1}')
    
    # Append the hash to the output file
    echo "$hash" >> "$output_file"
done

echo "SHA3-256 hashes for numbers 1 to 1000 have been saved to $output_file"

```

![3](https://github.com/user-attachments/assets/8acbeff1-45d0-4a71-9e8b-83eac1ea3f82)
