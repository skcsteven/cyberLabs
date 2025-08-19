# Flag Checker

50 pt REV for UIUCTF 2025

## Program Overview

Running the program shows me that it is a simple input checker as most rev challenges go.

In ghidra, here is the decompiled main function (I renamed variables based on function):

<img width="539" height="448" alt="image" src="https://github.com/user-attachments/assets/a7c2af48-391a-4995-b2ef-d90dd7e6a32e" />


The check_input essentially performs RSA encryption using modular exponentiation on a 32 bit value test_pt and checks to see if the result is equal to test_ct:

<img width="732" height="357" alt="image" src="https://github.com/user-attachments/assets/ed35b8cf-d1bb-4e7d-85a2-544f1ab0dc81" />

Function F that performs the modular exponentiation:

<img width="580" height="345" alt="image" src="https://github.com/user-attachments/assets/dea74d63-97a0-4c4d-b4fb-59336069b4e7" />


After looking at local variables, we are given the original message, ciphertext, n value in the following formula for RSA encryption:

    C = M ^ e mod n ------------ where C is the Cipher text and e and n are parts of public key.
    
Therefore, we must solve for the exponentiation variable e. This is what we input into the program.

## Solution

As mentioned before, we need to solve for the exponentiation variable, e, and this is possible through math. Specifically discrete logs.

If you only have one plaintext–ciphertext pair (m,c) and n you can try to recover e by solving:

e=discrete_logn(c,m)

That means: find the integer e such that 

m^e=c(mod n)

This is the discrete logarithm problem — which is hard in general, but with a small modulus (like 32-bit or 64-bit), it’s computationally feasible. Since the program asks for 8 groups of 32 bits, we can crack this challenge by solving for e for each chunk of the ciphertext, message pair.

Here is the python code that does exactly this and outputs 8 distinct inputs to be inputted when the executable is run:

```
#!/usr/bin/env python3
import struct
from math import isqrt

def unpck(byteArray):
   blocks = [struct.unpack("<I", bytes(byteArray[i:i+4]))[0] for i in range(0, len(byteArray), 4)]
   return blocks

def discrete_log(m, c, n):
    """
    Solve for e in m^e ≡ c (mod n) using Baby-step Giant-step algorithm.
    Returns e if found, else None.
    """
    m %= n
    c %= n

    if m == 0:
        return 0 if c == 0 else None

    # Step size
    k = isqrt(n) + 1

    # Baby steps: store (m^j mod n)
    baby_steps = {}
    value = 1
    for j in range(k):
        if value not in baby_steps:  # store only first occurrence
            baby_steps[value] = j
        value = (value * m) % n

    # Precompute m^-k mod n (using pow with -1 exponent requires gcd(m, n) = 1)
    try:
        m_inv_k = pow(m, -k, n)
    except ValueError:
        return None  # no modular inverse exists

    # Giant steps
    gamma = c
    for i in range(k + 1):
        if gamma in baby_steps:
            return i * k + baby_steps[gamma]
        gamma = (gamma * m_inv_k) % n

    return None

test_pt = [
    0xF5, 0xB1, 0x65, 0x22, 0x4A, 0x58, 0xB7, 0x91,
    0xDF, 0x6A, 0xF1, 0xD8, 0x30, 0x3E, 0x61, 0xCD,
    0xC4, 0xBB, 0x86, 0xC3, 0xD1, 0xC4, 0x27, 0x10,
    0x3C, 0x34, 0x4C, 0x41, 0x89, 0xEB, 0x2F, 0x1E
] # m

test_ct = [
    0x5E, 0xBF, 0x44, 0xDC, 0xEC, 0x1C, 0xFF, 0x5A,
    0xC2, 0xB4, 0xE9, 0xE1, 0x92, 0x9B, 0x32, 0x01,
    0x2A, 0xA9, 0x9C, 0x8F, 0xB4, 0xC5, 0x45, 0x0E,
    0x91, 0x4B, 0x4A, 0x60, 0x59, 0xEB, 0x81, 0x70
] # c

mess = unpck(test_pt)
cipher = unpck(test_ct)
mask = 0xffffff2f #n = p * q

res = []

for i in range(0,8):
   res.append(discrete_log(mess[i],cipher[i],mask))
   
ans = 0
for each in res:
   ans = (ans << 32) | each

print('8 blocks to input: ', res)

```
After running this script, you need to input the 8 inputs successively to retrieve the flag for this challenge.


## Resources & Learning

- https://www.geeksforgeeks.org/computer-networks/rsa-algorithm-cryptography/
