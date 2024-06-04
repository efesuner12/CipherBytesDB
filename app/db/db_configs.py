import app.operation.cryptography.file_encryption as file_decryptor

import os
import json

## Reads the encrypted configurations from the
# given path and decrypts the content 
# and returns a JSON 
def read_configs(path, password):

    try:
        path = os.path.expanduser(path)

        with open(path, "rb") as f:
            data = f.read()
            
        f.close()

        dec_data = file_decryptor.decrypt_file_data(data, password)

        db_configs = json.loads(dec_data) if len(dec_data) > 0 else None

        return db_configs
    except Exception:
        return None
