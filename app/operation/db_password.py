from app.db.database import Connected_Databases

import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor

## Gets the encrypted password of the given database
# and returns the decrypted password
def get_password(host, db_name, db_nick, error_msg):
    CONNECTED_DBS = Connected_Databases(error_msg)
    enc_password = CONNECTED_DBS.select_password(host, db_name)[0]

    password = aes_encryptor.decrypt(enc_password, error_msg) if enc_password else None

    return password
