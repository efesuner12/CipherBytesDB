import os
import hashlib
import hmac

## SHA-512 hash function with no salt
#
def sha_512_hash(data):
    sha512_hash_object = hashlib.sha512()
    sha512_hash_object.update(data.encode('utf-8'))
    hashed = sha512_hash_object.hexdigest()

    return hashed

## PBKDF2-HMAC salted SHA-512 hash function
#
def hash(data):
    salt = os.urandom(16)
    dt_hash = hashlib.pbkdf2_hmac('sha512', data.encode("utf-8"), salt, 100000)

    enc = salt + dt_hash

    return enc.hex()

## Compares the input string with the stored hash
# by extracting the hash bit of the stored hash
# and re hashing the input with the same salt and algrotihm
def validate(entered, stored):
    stored = bytes.fromhex(stored)

    ext_salt = stored[:16]
    ext_hash = stored[16:]

    entered_byte = bytes(entered, "utf-8")

    return hmac.compare_digest(
        ext_hash,
        hashlib.pbkdf2_hmac('sha512', entered_byte, ext_salt, 100000)
    )
