#!/bin/bash
echo "OMQEMDUEQMEK" > text.txt
for ((i = 0; i < 26; i++)); do
        /krypton/krypton2/encrypt text.txt
        cat ciphertext
        echo "   "
         > text.txt
        cat ciphertext >> text.txt
done
