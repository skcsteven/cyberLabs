## matryoshka by iamwololo	

Upon initial glance at the program with the file and strings command yields nothing of particular interest.

With the challenge name, I expect a lot of jumping around between layers!

### Program Function

The program takes a byte of data (our chr input) and uses that as a key to decrypt an executable file that it later runs.

This executable file turns out to be the same or very similar to the original program hence the name of the challenge.

The goal is to find the proper inputs for each "level" to decrypt the encrypted executables.

### Solution Process

start at the entry, use "start", set breakpoint there, examine and try to find out the arguments/parameter values

set breakpoints at the functions

Find and set breakpoint at main:
- calculate offset with ghidra
- add offset to start of program address found in pwndbg
- set breakpoint

```
#set breakpoint at main in pwndbg
pwndbg> vmmap
LEGEND: STACK | HEAP | CODE | DATA | WX | RODATA
             Start                End Perm     Size Offset File (set vmmap-prefer-relpaths on)
    0x555555554000     0x555555555000 r--p     1000      0 matryoshka


>>> hex(0x555555554000 + 0x11c9)
'0x5555555551c9'
```

Figure out what happens to my input:
- step through main and see that my input is entered into RAX and later deduce that it corresponds to the value that will be checked
- later in program this input (1 byte size) will be used to decrypt a string by xor'ing it with each byte in a string that will be written to a file
- need to figure out what input (byte) will decrypt the secret string and allow it to execute properly (expecting it to show the answer or success)

So the encrypted data needs to be decrypted by our one byte input and later executed, but how to figure out the key?

I know that each byte is xor'd with my one byte input and I learned that executable files all have the same header of 0x7f454c46, or 0x7f followed by ELF in ascii.

From here, I need to extract the first 4 bytes of the encrypted data using ghidra and find the value that when xor'd with the 4 bytes yields 0x7f454c46.

With the help of python, we see that the key value needs to be 15 in decimal or 0xf. But we don't just enter this because the key is derived from what we input. Analyzing the program shows us that it subs 0x57 from our input to yield the key so we simply add 0x57 to the key to come to our input of 'f'

```

#Deriving key

>>> desiredHeader = [0x7f, 0x45, 0x4c, 0x46]
>>> firstFourEncrypted = [0x70, 0x4A, 0x43, 0x49]
>>> firstFourEncrypted[0] ^ desiredHeader[0]
15
>>> firstFourEncrypted[1] ^ desiredHeader[1]
15
>>> firstFourEncrypted[2] ^ desiredHeader[2]
15
>>> firstFourEncrypted[3] ^ desiredHeader[3]
15
>>> hex(15)
'0xf'

#Deriving input

>>> chr(0x66)
'f'
>>> 0xf + 0x57
102
>>> chr(102)
'f'
```

When I use an input of 'f' a child process is started and I catch it in pwndbg:

```
#child process catch

process 4962 is executing new program: /proc/4962/exe
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".

#pwndbg setup
set follow-fork-mode child
```

I will fully decrypted the encrypted data now to see what kind of program the child process is:

```
#get address to examine encrypted data (find offset in ghidra, add to vmmap starting address)
>>> hex(0x555555554000+0x4080)
'0x555555558080'

#find the end range value by finding where the next local starts:
>>> hex(0x555555554000+0xea5f)
'0x555555562a5f'

#using math and subtracting the end range value with the beginning we get a size of 43488 bytes

#use extract the child process using the ranges calculated
pwndbg> dump memory child.bin 0x555555558080 0x555555562a5f
```

I will use a python script to decrypt the encrypted executable by xor'ing each byte with 0xf:


```
# Python script to decrypt encrypted executable
# works by xor'ing each byte with 0xf

with open("child.bin","rb") as f,  open("decrypted.bin", "wb") as new:
    while True:
        chunk = f.read(2000) # read up to 2000 bytes
        if not chunk:
            break
        new.write(bytes(b ^ 0x0f for b in chunk))
    print('done')

```

Now that I have the child executable, I can send it over to ghidra to see what it is doing.

Ok... so now I know why the challenge is called Matryoshka, the child executable is a spitting image of the parent except for the encrypted data is encrypted with a different xor key.

This time around the data is encrypted with a key of 11 in decimal or 0xb in hex. For the input, I add 0x57 to it and get the result of "b" in ascii

Now I will run the original program with 'fb' and cross my fingers that that is it.

It worked but another executable popped up. I repeat the same process as above to find the 3rd key of "3" (30 is added to the key instead of 57 this time)

Analyzing the 4th executable we see:

```
  iVar1 = atoi(*(char **)(param_2 + 8));
  if (iVar1 == 9) {
    puts("u win good job!!!!");
  }
```

So to solve this challenge the input comes out to "fb39"

### What did I learn from this challenge?

- practical pwndbg/ghidra skills
   -  Offset calculations and breakpoints
   -  reading registers
- ELF file format/headers
- Stack characteristics

