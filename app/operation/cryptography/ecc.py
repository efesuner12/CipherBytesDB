from tinyec import registry, ec

import os
import secrets
import hashlib

DIRECTORY_PATH = os.path.expanduser("~/.cipherbytesdb/")
CURVE = registry.get_curve('brainpoolP256r1')

## Generates a private and public key
# pair from the set Elliptic Curve
def generate_key_pair():
    priv_key = secrets.randbelow(CURVE.field.n)
    pub_key = priv_key * CURVE.g

    return priv_key, pub_key

## Converts the EC point into an 256-bit key
# by hashing it
def point_to_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))

    return sha.digest()

## Converts a EC point to bytes
#
def point_to_bytes(point):
    x_bytes = int.to_bytes(point.x, 32, 'big')
    y_bytes = int.to_bytes(point.y, 32, 'big')

    return x_bytes + y_bytes

## Converts bytes to a EC point
#
def bytes_to_point(byte_data):
    x = int.from_bytes(byte_data[:32], 'big')
    y = int.from_bytes(byte_data[32:], 'big')

    return ec.Point(CURVE, x, y)

## Writes the key pair to their files by converting them to bytes
#
def write_key_pair(metadata, priv_key, pub_key, error_msg):
    
    try:
        priv_key_path = DIRECTORY_PATH + f"{metadata}"

        # Convert int into bytes
        byte_priv_key = (priv_key).to_bytes((priv_key.bit_length() + 7) // 8, 'big')

        with open(priv_key_path, "wb") as f:
            f.write(byte_priv_key)

        f.close()

        pub_key_path = DIRECTORY_PATH + f"{metadata}.pub"

        # Convert EC point into bytes
        byte_pub_key = point_to_bytes(pub_key)

        with open(pub_key_path, "wb") as f:
            f.write(byte_pub_key)

        f.close()

        return True
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return False

## Deletes the key pair files
#
def delete_key_pair(metadata, error_msg):
    
    try:
        priv_key_path = DIRECTORY_PATH + f"{metadata}"
        pub_key_path = DIRECTORY_PATH + f"{metadata}.pub"

        os.remove(priv_key_path)
        os.remove(pub_key_path)

        return True
    except FileNotFoundError:
        error_msg.set("Files not found")
        return False
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return False

## Reads the byte public key from the file and
# converts it to EC point
def read_public_key(metadata, error_msg):
    
    try:
        pub_key_path = DIRECTORY_PATH + f"{metadata}.pub"

        with open(pub_key_path, "rb") as f:
            pub_key = f.read()
            
        f.close()

        # Convert bytes to EC point
        return bytes_to_point(pub_key)
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return None

## Reads the byte private key from the file and
# converts it to int
def read_private_key(metadata, error_msg):
    
    try:
        priv_key_path = DIRECTORY_PATH + f"{metadata}"

        with open(priv_key_path, "rb") as f:
            priv_key = f.read()
            
        f.close()

        # Convert bytes to int
        return int.from_bytes(priv_key, byteorder='big')
    except Exception:
        error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
        return None
