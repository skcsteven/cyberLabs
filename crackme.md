# Basic ? crackme - rootme 25 pts

_Don't let yourself be knocked down by this poor binary_

This is a basic binary that will get a "Key" and check the input.

Calling strings on the executable doesn't yield any simple answers so I will decompile it and take a look in Ghidra.

Our input is checked with the check function:

---

The key value is 0x950A943E7F4F96A8 and the value checked against our XOR'd input is 
-0x5c8852a8fb9a0207 or 0xa377ad570465fdf9 in twos complement.

By XOR logic, we just need to XOR the key with the check value to get the proper input. Using python results in the input value of 0x367d39697b2a6b51. Now to enter the password...

Looking at how inputs are handled in GDB, we see that they are always set to string type. So we need to find ASCII values that result in the hex of 0x367d39697b2a6b51.

This python script does the heavy lifting for us:

```
import struct

# Convert 0x367d39697b2a6b51 into little-endian byte order
desired_value = 0x367d39697b2a6b51
input_bytes = struct.pack("<Q", desired_value)  # Little-endian (assuming x86/x86_64 architecture)

# Print the corresponding string representation
print(input_bytes.decode('latin-1'))  # Use 'latin-1' to preserve raw byte values
```

This gives us the correct key: Qk*{i9}6 

Not so fast... this works when the program is run in GDB or a debugger but when I run the program normally this key is incorrect and thus not the correct password for the crackme.

Running strace on the executable yields this line:

```
ptrace(PTRACE_TRACEME)                  = -1 EPERM (Operation not permitted)

```
This means that the program is checking for a debugger and likely runs differently.

The difference between running in a debugger vs without impacts the "key" value used in the XOR.

So we need to extract the correct key value and use that to find the password. To do this we need to extract the symbol "key" from the binary and find its value.

First, we will view the runtime address of "key". Next, we need to find the base address of the executable. From there we can inspect the proper address (key address plus base address) value and we have the key. The process in linux is below:

```
┌──(kali㉿kali)-[~/Documents/rootme/crackme]
└─$ readelf -sW ./ch73.bin | grep key   
    13: 0000000000004048     8 OBJECT  GLOBAL DEFAULT   24 key
                                                                        
┌──(kali㉿kali)-[~/Documents/rootme/crackme]
└─$ pgrep ch73.bin
97288
729587
1405374
1477573
                                                                        
┌──(kali㉿kali)-[~/Documents/rootme/crackme]
└─$ cat /proc/97288/maps | grep ch73.bin
5598d03b7000-5598d03b8000 r--p 00000000 08:01 2521859                    /home/kali/Documents/rootme/crackme/ch73.bin
5598d03b8000-5598d03b9000 r-xp 00001000 08:01 2521859                    /home/kali/Documents/rootme/crackme/ch73.bin
5598d03b9000-5598d03ba000 r--p 00002000 08:01 2521859                    /home/kali/Documents/rootme/crackme/ch73.bin
5598d03ba000-5598d03bb000 r--p 00002000 08:01 2521859                    /home/kali/Documents/rootme/crackme/ch73.bin
5598d03bb000-5598d03bc000 rw-p 00003000 08:01 2521859                    /home/kali/Documents/rootme/crackme/ch73.bin
                                                                        
┌──(kali㉿kali)-[~/Documents/rootme/crackme]
└─$ objdump -s --section=.data ./ch73.bin     

./ch73.bin:     file format elf64-x86-64

Contents of section .data:
 4030 00000000 00000000 38400000 00000000  ........8@......
 4040 00000000 00000000 a8964f7f 3e940a95  ..........O.>...
                                                        
┌──(kali㉿kali)-[~/Documents/rootme/crackme]
└─$ sudo dd if=/proc/97288/mem bs=1 skip=$((0x5598d03bb048)) count=8 2>/dev/null | hexdump -C
[sudo] password for kali: 
00000000  b1 97 56 7e 27 95 13 94                           |..V~'...|
00000008

```

So the key value is 0x941395277e5697b1 (LSB is a pain sometimes). From here we can xor this value with the 2's complement of the check value to get our password. Below is the python script to do this for us and give us our PASSWORD:

```
import struct

check = -0x5c8852a8fb9a0207
c = (1 << 64) + check
key = 0x941395277e5697b1
password = key^c

print('check \t', check,hex(check))
print('c\t',c,hex(c))
print('key \t',key, hex(key))
print('key^c & passwd',password, hex(password))

print('is it right?\t', key^(password), hex(key^(password)))

input_bytes = struct.pack("<Q", password)  # Little-endian (assuming x86/x86_64 architecture)

# Print the corresponding string representation
print('PASSWORD\t',input_bytes.decode('latin-1'))  # Use 'latin-1' to preserve raw byte values

'''
OUTPUT:

check    -6667670134051176967 -0x5c8852a8fb9a0207
c        11779073939658374649 0xa377ad570465fdf9
key      10670035939026704305 0x941395277e5697b1
key^c & passwd 3991377225494784584 0x376438707a336a48
is it right?     11779073939658374649 0xa377ad570465fdf9 # matches the c value
PASSWORD         Hj3zp8d7
'''
```

## References/Learning

	- 2's complement
	- signed vs unsigned
	- runtime/base addresses
	- XOR