from app.operation.cryptography.db_encryption import Database_Encrypter
from app.operation.access_control import Access_Control

import app.operation.cryptography.aes as aes_encryptor

## Implements Row Level Encryption (RLE)
#
class Row_Encrypter(Database_Encrypter):

    def __init__(self, db_data_pack, table_name):
        # Inherits from Database_Encryptor - uses its variables and functions
        super().__init__(db_data_pack)

        self.TABLE_NAME = table_name
        self.TABLE_PRIMARY_KEY = ""
        self.CELL_ENC_MODEL = "2"

        self.access_control = Access_Control(db_data_pack, table_name)

    ## Encrypts the given row
    # Performs the whole operation
    # + Gets the primary key column name
    # + Gets all columns of the table
    # + Gets the plaintexts
    # + Removes the primary key column from the list of columns
    # to be encrypted and the corresponding plaintext (0)
    # + Generates the metadata
    # + Generates the encryption key and gets its ID
    # + Creates the access control rules
    # + For column in all columns
    # ++ Generates the nonce
    # ++ Encrypt
    # ++ Generates the SQL statement to update the cell
    # ++ If current field type is varchar and its len is greater than the ciphertext's
    # +++ Updates the table with the ciphertext
    # +++ Updates the column data type
    # ++ Else
    # +++ Updates the column data type and writes the ciphertext
    # This is a strategy followed to avoid format and length errors
    def encrypt_row(self, row_id, users, error_msg):
        try:
            self.TABLE_PRIMARY_KEY = self.get_primary_key_column(error_msg)
            
            all_columns = self.get_all_columns(error_msg)

            if self.TABLE_PRIMARY_KEY == None or len(all_columns) == 0:
                return False

            plaintexts = list(self.get_row_values(row_id, error_msg)[0])
            
            if plaintexts:
                tmp_prim_key = (self.TABLE_PRIMARY_KEY,)
                all_columns.remove(tmp_prim_key)
                plaintexts.pop(0)

                hashed_metadata = self.generate_metadata(row_id)
                key, key_id = self.generate_enc_key(hashed_metadata, error_msg)

                ac_rules = [(user, key_id) for user in users]
                ac_rules_created = self.access_control.add_ac_rule(ac_rules, error_msg)

                if not ac_rules_created:
                    return False

                for i in range(len(all_columns)):
                    column_name = all_columns[i][0]
                    plaintext = plaintexts[i]

                    nonce = self.generate_enc_nonce()
                    ciphertext = aes_encryptor.encrypt(str(plaintext), hashed_metadata, key, nonce, error_msg)

                    if ciphertext:
                        sql_ct = [f"UPDATE {self.TABLE_NAME} SET {column_name} = '{ciphertext}' WHERE {self.TABLE_PRIMARY_KEY} = '{row_id}'"]

                        current_field_type = self.get_field_type(column_name, error_msg)
                        field_type = current_field_type[0]
                        field_length = current_field_type[1]
                        field_length = int(field_length) if field_length else 0

                        cipher_length = len(ciphertext)
                        cipher_length = 64 if cipher_length < 64 else cipher_length

                        # If field type is VARCHAR and its length is greater than ciphertext length
                        # then write ciphertext then update the field type
                        if field_type == "varchar" and field_length > cipher_length:
                            ciphertext_written = self.write_to_table(sql_ct, error_msg)

                            field_updated = self.update_field_type(column_name, cipher_length, error_msg) if ciphertext_written else False
                            
                            if field_updated:
                                continue

                            error_msg.set(f"There has been a problem with column: {column_name}")
                            return False

                        # If field length is less than ciphertext length
                        # then update field type first then write the ciphertext
                        field_updated = self.update_field_type(column_name, cipher_length, error_msg)

                        ciphertext_written = self.write_to_table(sql_ct, error_msg) if field_updated else False

                        if ciphertext_written:
                            continue

                        error_msg.set(f"There has been a problem with column: {column_name}")
                        return False

                    return False

                return True

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
    # (skips the 0th item as it is the unencrypted primary key value)
    # ++ Decrypts the data
    def decrypt_row(self, row_id, error_msg):
        try:
            if not self.TABLE_PRIMARY_KEY:
                self.TABLE_PRIMARY_KEY = self.get_primary_key_column(error_msg)

            ciphertexts = self.get_row_values(row_id, error_msg)[0]

            plaintexts = []
            hashed_metadata = None

            if ciphertexts:
                hashed_metadata = self.generate_metadata(row_id)

                for i in range(1,len(ciphertexts)):
                    ciphertext = ciphertexts[i]
                    plaintext = aes_encryptor.decrypt(ciphertext, error_msg)
                    plaintext = None if plaintext == 'None' else plaintext
                    plaintexts.append(plaintext)

            return plaintexts, hashed_metadata
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None, None
