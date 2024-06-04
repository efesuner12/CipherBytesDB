from app.operation.cryptography.db_encryption import Database_Encrypter
from app.operation.access_control import Access_Control

import app.operation.cryptography.aes as aes_encryptor

## Implements Column Level Encryption (CLE)
#
class Column_Encrypter(Database_Encrypter):
    
    def __init__(self, db_data_pack, table_name):
        # Inherits from Database_Encryptor - uses its variables and functions
        super().__init__(db_data_pack)

        self.TABLE_NAME = table_name
        self.COLUMN_ENC_MODEL = "1"

        self.access_control = Access_Control(db_data_pack, table_name)

    ## Encrypts the given column
    # Performs the whole operation
    # + Abort if the column is a master foreign key column
    # + Gets the primary key column name
    # + Gets the primary key column values
    # + Gets the plaintexts
    # + Gets the current field type and length
    # + Generates the metadata
    # + Generates the key and gets its ID
    # + Creates the access control rules
    # + For each plaintext
    # ++ Fetches the primary column value
    # ++ Generates a nonce
    # ++ Encrypts the data
    # ++ Generates the SQL statement to update the table with the ciphertext for a bulk update
    # + Gets the max ciphertext length
    # + If current field type is varchar and its len is greater than the ciphertext's
    # ++ Updates the table with the ciphertext
    # ++ Updates the column data type
    # + Else
    # ++ Updates the column data type and writes the ciphertext
    # This is a strategy followed to avoid format and length errors
    def encrypt_column(self, column_name, users, error_msg):
        try:
            # Return False column in it's a master foreign key column
            if self.is_master_foreign_column(column_name, error_msg):
                error_msg.set("Columns that are 'master' foreign keys cannot be encrypted due to MySQL restrictions")
                return False

            PRIMARY_COLUMN = self.get_primary_key_column(error_msg)                
            primary_column_results = self.get_column_values(PRIMARY_COLUMN, PRIMARY_COLUMN, error_msg)

            if PRIMARY_COLUMN and primary_column_results:
                plaintexts = self.get_column_values(column_name, PRIMARY_COLUMN, error_msg)

                if plaintexts:
                    current_field_type = self.get_field_type(column_name, error_msg)
                    field_type = current_field_type[0]
                    field_length = current_field_type[1]
                    field_length = int(field_length) if field_length else 0

                    hashed_metadata = self.generate_metadata(column_name)
                    key, key_id = self.generate_enc_key(hashed_metadata, error_msg)

                    ac_rules = [(user, key_id) for user in users]
                    ac_rules_created = self.access_control.add_ac_rule(ac_rules, error_msg)

                    if not ac_rules_created:
                        return False

                    ciphertexts = []
                    sql_ct = []

                    for i in range(len(plaintexts)):
                        value = plaintexts[i][0]
                        primary_key = primary_column_results[i][0]

                        nonce = self.generate_enc_nonce()

                        ciphertext = aes_encryptor.encrypt(str(value), hashed_metadata, key, nonce, error_msg)

                        if ciphertext:
                            ciphertexts.append(ciphertext)
                            sql_ct.append(f"UPDATE {self.TABLE_NAME} SET {column_name} = '{ciphertext}' WHERE {PRIMARY_COLUMN} = '{primary_key}'") if primary_key else None

                    cipher_length = max(len(item) for item in ciphertexts) if len(ciphertexts) > 0 else 0
                    cipher_length = 64 if cipher_length < 64 else cipher_length

                    # If field type is VARCHAR and its length is greater than ciphertext length
                    # then write ciphertext then update the field type
                    if field_type == "varchar" and field_length > cipher_length:
                        ciphertext_written =  self.write_to_table(sql_ct, error_msg)

                        return self.update_field_type(column_name, cipher_length, error_msg) if ciphertext_written else False

                    # If field length is less than ciphertext length
                    # then update field type first then write the ciphertext
                    field_updated = self.update_field_type(column_name, cipher_length, error_msg)
                    return self.write_to_table(sql_ct, error_msg) if field_updated else False
            
            return False
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Decrypts the given column
    # Only performs the decryption of the ciphertexts
    # nothing more
    # + Gets the ciphertexts
    # + Generates the metadata
    # + For each ciphertext
    # ++ Decrypts the data
    def decrypt_column(self, column_name, error_msg):
        try:
            PRIMARY_COLUMN = self.get_primary_key_column(error_msg)
            ciphertexts = self.get_column_values(column_name, PRIMARY_COLUMN, error_msg)

            plaintexts = []
            hashed_metadata = None

            if ciphertexts:
                hashed_metadata = self.generate_metadata(column_name)

                for i in range(len(ciphertexts)):
                    ciphertext = ciphertexts[i][0]
                    plaintext = aes_encryptor.decrypt(ciphertext, error_msg)
                    plaintext = None if plaintext == 'None' else plaintext
                    plaintexts.append(plaintext)

            return plaintexts, hashed_metadata
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None, None
