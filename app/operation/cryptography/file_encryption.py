from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import app.operation.cryptography.hash as hasher

import os

## Generates 256-bit password based key
# using Scrypt kdf
def generate_password_key(password, salt):
    try:
        salt = os.urandom(16) if salt is None else salt

        kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1, backend=default_backend())
        key = kdf.derive(password)

        return salt, key
    except Exception:
        return None, None

## Implements AES-256 GCM encryption
# with AAD of the nonce, metadata and salt
def encrypt(data, metadata, key, nonce, salt):
    try:
        encryptor = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend()).encryptor()
                
        aad = nonce + metadata + salt
        encryptor.authenticate_additional_data(aad)

        ciphertext = encryptor.update(data.encode("utf-8"))
        ciphertext += encryptor.finalize()

        header = aad + encryptor.tag

        return header + ciphertext
    except Exception:
        return None

## Encrypts the content of the given file
# and writes the ciphertext to the file
def encrypt_file_data(path, data, password):

    hashed_metadata = bytes.fromhex(hasher.sha_512_hash(path))

    salt, key = generate_password_key(password.encode("utf-8"), None)

    nonce = os.urandom(12)

    ciphertext = encrypt(data, hashed_metadata, key, nonce, salt)
    
    with open(path, 'wb') as f:
        f.write(ciphertext)
    
    f.close()

## ## Implements AES-256 GCM decryption
# with metadata, nonce and salt authentication
# and re creates the password based key using Scrypt KDF
def decrypt_file_data(ciphertext, password):
    try:
        aad = ciphertext[0:92]
        nonce = aad[0:12]
        metadata = aad[12:76]
        salt = aad[76:92]
        tag = ciphertext[92:108]

        salt, key = generate_password_key(password.encode("utf-8"), salt)

        decryptor = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend()).decryptor()

        decryptor.authenticate_additional_data(aad)

        plaintext = decryptor.update(ciphertext[108:])
        plaintext += decryptor.finalize()
        
        return plaintext.decode("utf-8")
    except Exception:
        return None
