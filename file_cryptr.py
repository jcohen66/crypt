import crypto
import os
import random
import struct
import sys
import argparse
from Crypto.Cipher import AES


def encrypt(key, filename, chunksize=64*1024):
    if filename.endswith('.aes'):
        print('[-] File already encrypted. Aborting...')

    if not os.path.exists(filename):
        print('[-] File: ' + filename + ' does not exist.')
        exit(-1)

    out_filename = filename + '.aes'
    print(out_filename)

    iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(filename)

    with open(filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += (' ' * (16 - len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))

    os.remove(filename)


def decrypt(key, filename, chunksize=24*1024):
    if not filename.endswith('.aes'):
        print("[-] Must have a file with extension '.aes' to decrypt.")
        exit(-1)

    if not os.path.exists(filename):
        print('[-] File: ' + filename + ' does not exist.')
        exit(-1)

    out_filename = filename.replace('.aes', '')

    with open(filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)

    os.remove(filename)


def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", help="ENCRYPT/DECRYPT")
    parser.add_argument("-i", "--input", help="input file required")
    parser.add_argument("-k", "--key", help="minimum 16 char key required")

    args = parser.parse_args()

    if args.action is None:
        print('[-] Must supply -a ENCRYPT/DECRYPT action.')
        exit(-1)

    if args.input is None:
        print('[-] Input file required.')
        exit(-1)

    if args.key is None or len(args.key) < 16:
        print('[-] Minimum 16 character encryption key required".')
        exit(-1)

    if args.action.upper() == 'ENCRYPT':
        encrypt(args.key, args.input)
    elif args.action.upper() == 'DECRYPT':
        decrypt(args.key, args.input)
    else:
        print('[-] Must supply -a ENCRYPT/DECRYPT action.')


if __name__ == "__main__":
    main(sys.argv[1:])
