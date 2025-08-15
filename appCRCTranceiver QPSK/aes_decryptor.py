from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Util.Padding import pad, unpad
import argparse
import os

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def decrypt_file(input_path, output_path, key_path):
    with open(key_path, 'rb') as f:
        key = f.read()

    with open(input_path, 'rb') as f:
        iv = f.read(16)
        ciphertext = f.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext))

    with open(output_path, 'wb') as f:
        f.write(plaintext)

    print(f"AES decrypted file saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", required=True)
    parser.add_argument("--outfile", required=True)
    parser.add_argument("--keyfile", required=True)
    args = parser.parse_args()
    decrypt_file(args.infile, args.outfile, args.keyfile)
