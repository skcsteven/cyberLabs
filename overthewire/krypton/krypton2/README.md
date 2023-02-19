# Krypton 2 to 3
This level was interesting because a caeser cipher encrypted string was given to me that I had to crack.
To crack the caeser cipher I created by first ever bash script - nothing too special - that essentially brute forced my way.

## General process
The README file in the /krypton/krypton2 directory gives example usage of the "encrypt" command within the same directory: 

![image](https://user-images.githubusercontent.com/65736346/219907770-5dbfb324-252d-41e7-9f59-1067a8a6d20e.png)

After seeing this, I decided to create a brute force bash script that would repeatedly use the "encrypt" tool on the encrypted password string within the krypton3 file.

Bash script:

https://github.com/skcsteven/cyberFun/blob/1cf9f6c08517f1cf4f8a50fb743139b11d78407c/overthewire/krypton/krypton2/firstBashEver.sh#L1-L9

The results from running:

![image](https://user-images.githubusercontent.com/65736346/219908173-3b84c2d0-884a-4de8-a642-8424ef937710.png) 

A quick look at the output and the only intelligible decoded string seems to be the password for the next level.
