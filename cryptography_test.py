from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(input_file_path, output_file_path, key):
    # Read the input file
    with open(input_file_path, 'rb') as file:
        data = file.read()

    # Generate a random initialization vector
    iv = os.urandom(16)

    # Create a Cipher object for AES encryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_data = encryptor.update(data) + encryptor.finalize()

    # Write the iv and encrypted data to the output file
    with open(output_file_path, 'wb') as file:
        file.write(iv + encrypted_data)


def decrypt_file(input_file_path, output_file_path, key):
    # Read the encrypted data
    with open(input_file_path, 'rb') as file:
        iv = file.read(16)  # The first 16 bytes are the IV
        encrypted_data = file.read()

    # Create a Cipher object for AES decryption
    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the data
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Write the decrypted data to the output file
    with open(output_file_path, 'wb') as file:
        file.write(decrypted_data)

def main():
    key = os.urandom(32)  # AES-256 key
    encrypt_file('cryptograhy_file.txt', 'encrypted_file.enc', key)

    print("Encryption completed. Key (keep this safe!):", key.hex())

    decrypt_file('encrypted_file.enc', 'decrypted_file.txt', key)

    print("Decryption completed.")

if __name__ == "__main__":
    main()
