import crypto
import os
import random
import struct
import sys
import argparse
from Crypto.Cipher import AES
import Crypto.Random
import hashlib

# Salt size in bytes
SALT_SIZE = 16

# Number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20

# Size multiple required for AES
AES_MULTIPLE = 16


def iv():
    return ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

def generate_key_sha256(password, salt, iterations):
    assert iterations > 0

    key = password + salt

    for i in range(iterations):
        key = hashlib.sha256(key).digest()

    return key

def generate_key_plaintext(size, special_chars=True):

    CHARS = ['1','2','3','4','5','6','7','8','9','0', \
    'A','B','C','D','E','F','G','H','I','J','K','L','M', \
    'N','O','P','Q','R','S','T','U','V','W','X','Y','Z', \
    'a','b','c','d','e','f','g','h','i','j','k','l','m', \
    'n','o','p','q','r','s','t','u','v','w','x','y','z']

    SPECIAL_CHARS = ['~','!','@','#','$','%','^','&','*', \
    '(',')','-','_','+','[',']','?']

    if(special_chars):
        CHARS += SPECIAL_CHARS

    setsize = len(CHARS)
    key = ''
    for i in range(size):
        r = random.randint(0, setsize-1)
        key += CHARS[r]

    return key

def encrypt(key, iv, plaintext):
    aes = AES.new(key, AES.MODE_CBC, iv)
    encd = aes.encrypt(plaintext)
    return encd


def decrypt(key, iv, ciphertext):
    aes = AES.new(key, AES.MODE_CBC, iv)
    plaintext = aes.decrypt(ciphertext)
    return plaintext


iv = iv()
key = 'abcDEF1234567890'
data = 'hello world 1234'  # <- 16 bytes
print(decrypt(key, iv, encrypt(key, iv, data)))


gen = generate_key_plaintext(64,False)
print(gen)

salt = Crypto.Random.get_random_bytes(SALT_SIZE)

print(generate_key_sha256(gen, salt, NUMBER_OF_ITERATIONS))