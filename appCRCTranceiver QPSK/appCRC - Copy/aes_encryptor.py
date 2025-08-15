from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
import argparse
import os

def pad(data):
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len]) * pad_len

def encrypt_file(input_path, output_path, key_path):
    key = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC)
    iv = cipher.iv

    with open(input_path, 'rb') as f:
        data = f.read()
    padded = pad(data)
    ciphertext = cipher.encrypt(padded)

    with open(output_path, 'wb') as f:
        f.write(iv + ciphertext)
    
    with open(key_path, 'wb') as f:
        f.write(key)

    print(f"AES encrypted file saved to: {output_path}")
    print(f"AES key saved to: {key_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", required=True)
    parser.add_argument("--outfile", required=True)
    parser.add_argument("--keyfile", required=True)
    args = parser.parse_args()
    encrypt_file(args.infile, args.outfile, args.keyfile)
