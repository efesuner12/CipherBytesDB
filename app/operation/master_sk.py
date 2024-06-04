from app.operation.ekms_api import EKMS_API

import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor

## Creates the master symmetric key for JWT if
# not already created
# Return True if key created or already exists
def create_master_sk(error_msg):
    metadata = "cipherbytesdb#jwt#master"
    hashed_metadata = hasher.sha_512_hash(metadata)

    ekms = EKMS_API(error_msg)
    sk_exists = ekms.check_key_existance(hashed_metadata)

    if sk_exists is None:
        return False

    master_sk = None

    if not sk_exists:
        master_sk = aes_encryptor.generate_key(hashed_metadata, "Monthly", error_msg)

    return True if master_sk is not None or sk_exists else False
