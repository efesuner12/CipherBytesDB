from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

import os

from app.operation.ekms_api import EKMS_API

import app.operation.cryptography.ecc as ecc

## Re constructs the encryption key by
# fetching the encryption public key from the EKMS
# and reading the user key pair 
# and calculates the encryption key
# Will be used in connected databases and API authentication
def generate_encryption_key(metadata, error_msg):
    try:
        ekms = EKMS_API(error_msg)

        enc_pub_key_hex = ekms.get_pub_key(metadata)
        enc_pub_key_hex = enc_pub_key_hex[0]
        enc_pub_key_byte = bytes.fromhex(enc_pub_key_hex)
        enc_pub_key = ecc.bytes_to_point(enc_pub_key_byte)

        user_priv_key = ecc.read_private_key(metadata, error_msg)
        user_pub_key = ecc.read_public_key(metadata, error_msg)

        enc_key = user_priv_key * enc_pub_key
        enc_key = ecc.point_to_key(enc_key)

        return enc_key, user_priv_key, user_pub_key
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return None

## Generates 96-bit nonce
#
def generate_nonce():
    return os.urandom(12)

## Generates an encryption EC key pair and an user EC key pair
# Writes the user key pair to their files and calculates the 
# 256-bit symmetric key
# Posts the encryption private and public key pair to the EKMS
def generate_key(metadata, key_rotation_interval, error_msg):
    enc_priv_key, enc_pub_key = ecc.generate_key_pair()

    user_priv_key, user_pub_key = ecc.generate_key_pair()
    is_written = ecc.write_key_pair(metadata, user_priv_key, user_pub_key, error_msg)

    if not is_written:
        return None

    enc_key = user_priv_key * enc_pub_key
    enc_key = ecc.point_to_key(enc_key)

    # Convert point to hex
    enc_pub_key_hex = ecc.point_to_bytes(enc_pub_key).hex()

    ekms = EKMS_API(error_msg)

    return enc_key if ekms.post_key_pair(enc_priv_key, enc_pub_key_hex, metadata, key_rotation_interval) else None

## Implements AES-256 GCM encryption
# with AAD of the nonce and the metadata
def encrypt(data, metadata, key, nonce, error_msg):
    try:
        encryptor = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend()).encryptor()
        
        metadata = bytes.fromhex(metadata)
        
        aad = nonce + metadata
        encryptor.authenticate_additional_data(aad)

        ciphertext = encryptor.update(data.encode("utf-8"))
        ciphertext += encryptor.finalize()

        header = aad + encryptor.tag

        return (header + ciphertext).hex()
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return None

## Re constructs the decryption key by 
# fetcheing the encryption private key from EKMS
# reading the user public key from the file
# and calculating the decryption key
def generate_decryption_key(metadata, error_msg):
    try:
        # Fetching the key will fail if the ciphertext
        # has been tempered with
        ekms = EKMS_API(error_msg)

        enc_priv_key = ekms.get_priv_key(metadata)
        enc_priv_key = int(enc_priv_key[0])

        user_pub_key = ecc.read_public_key(metadata, error_msg)

        dec_key = user_pub_key * enc_priv_key
        dec_key = ecc.point_to_key(dec_key)

        return dec_key
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return None

## Implements AES-256 GCM decryption
# with metadata and nonce authentication
def decrypt(ciphertext, error_msg):
    try:
        byte_ciphertext = bytes.fromhex(ciphertext) if type(ciphertext) is str else ciphertext

        aad = byte_ciphertext[0:76]
        nonce = aad[0:12]
        metadata = aad[12:76].hex()
        tag = byte_ciphertext[76:92]

        dec_key = generate_decryption_key(metadata, error_msg)

        decryptor = Cipher(algorithms.AES(dec_key), modes.GCM(nonce, tag), backend=default_backend()).decryptor()

        decryptor.authenticate_additional_data(aad)

        plaintext = decryptor.update(byte_ciphertext[92:])
        plaintext += decryptor.finalize()
        
        return plaintext.decode("utf-8")
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return None
