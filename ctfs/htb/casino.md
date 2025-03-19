# FlagCasino - htbctf rev 975

The team stumbles into a long-abandoned casino. As you enter, the lights and music whir to life, and a staff of robots begin moving around and offering games, while skeletons of prewar patrons are slumped at slot machines. A robotic dealer waves you over and promises great wealth if you can win - can you beat the house and gather funds for the mission?

Simple executable that asks for bets and takes user input:

![example](https://github.com/user-attachments/assets/747ccf1b-9473-4a40-aafe-a2503a5a781b)

Decompiled code:

![ghidradecompile](https://github.com/user-attachments/assets/582a61da-c4f0-4587-8b26-1aeb9645f050)


Looking at the decompiled code in ghidra tells me the program runs like this:

Get user input -> use it as a seed for rand()

Take the random value produced by the seed and compare it to a value stored in the "check" array at a certain index.

This index increments by 4 bytes each time it loops through to get a different value in the check array.

These values in the check array are equivalent to the randomized values when you use the ASCII 0-255 (uint8) range as seeds.

So inputting each character one by one, we are piecing together the flag.

Python solution from Motasem Hamdan:

```
import ctypes
from pwn import *

libc = ctypes.CDLL('libc.so.6')

mapping = {}

for i in range(255):
    libc.srand(i)
    mapping[libc.rand()] = chr(i)

flag = ""
casino = ELF("./casino", checksec=False)

for b in range(29):
    val = casino.u32(casino.sym["check"] + b * 4)
    flag += mapping[val]
    
print(flag)
```


## Ref/learning
- ghidra
- walkthrough https://motasemhamdan.medium.com/hackthebox-flag-casino-reverse-engineering-ctf-writeups-2247bc6dafee
