# crypt

**File Encryption**

python file_cryptr.py -a encrypt -i /home/kaiser/Downloads/a49fa21e.jpg -k 0123456789abcdef

python file_cryptr.py -a decrypt -i /home/kaiser/Downloads/a49fa21e.jpg.aes -k 0123456789abcdef

**String Encryption**

```
iv = iv()
key = 'abcDEF1234567890'
data = 'hello world 1234'  # <- 16 bytes
print(decrypt(key, iv, encrypt(key, iv, data)))
```
