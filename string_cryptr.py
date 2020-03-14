import crypto
import os
import random
import struct
import sys
import argparse
from Crypto.Cipher import AES


def iv():
    return ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])


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
