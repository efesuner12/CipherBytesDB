from app.operation.cryptography.db_encryption import Database_Encrypter
from app.operation.access_control import Access_Control

import app.operation.cryptography.aes as aes_encryptor

## Implements Table Level Encryption (TLE)
#
class Table_Encrypter(Database_Encrypter):
    
    def __init__(self, db_data_pack, table_name):
        # Inherits from Database_Encryptor - uses its variables and functions
        super().__init__(db_data_pack)

        self.TABLE_NAME = table_name
        self.COLUMN_ENC_MODEL = "0"
        self.all_columns = []

        self.access_control = Access_Control(db_data_pack, table_name)

    ## Encrypts the table
    # Performs the whole operation
    # + Gets all columns of the table
    # + Generates the metadata
    # + Generates the key and gets its ID
    # + Creates the access control rules
    # + Gets the primary key column name
    # + Gets the primary key column values
    # + Moves the primary key column in the all columns list
    # to last - otherwise primary values will change and 
    # writing ciphertexts on other columns will fail
    # + For each column of the table
    # ++ Implements CLE
    def encrypt_table(self, users, error_msg):
        try:
            self.all_columns = self.get_all_columns(error_msg)

            hashed_metadata = self.generate_metadata("")
            key, key_id = self.generate_enc_key(hashed_metadata, error_msg)

            ac_rules = [(user, key_id) for user in users]
            ac_rules_created = self.access_control.add_ac_rule(ac_rules, error_msg)

            if not ac_rules_created:
                return False

            PRIMARY_COLUMN = self.get_primary_key_column(error_msg)            
            primary_column_results = self.get_column_values(PRIMARY_COLUMN, PRIMARY_COLUMN, error_msg)

            if PRIMARY_COLUMN == None or primary_column_results == None:
                return False

            index_to_move = next(i for i, tpl in enumerate(self.all_columns) if tpl[0] == PRIMARY_COLUMN)
            self.all_columns.append(self.all_columns.pop(index_to_move))
            
            for column in self.all_columns:
                column_name = column[0]

                # Skip column if it's a master foreign key column
                if self.is_master_foreign_column(column_name, error_msg):
                    continue

                plaintexts = self.get_column_values(column_name, PRIMARY_COLUMN, error_msg)

                if plaintexts:
                    current_field_type = self.get_field_type(column_name, error_msg)
                    field_type = current_field_type[0]
                    field_length = current_field_type[1]
                    field_length = int(field_length) if field_length else 0

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

                        field_updated = self.update_field_type(column_name, cipher_length, error_msg) if ciphertext_written else False

                        if field_updated:
                            continue

                        error_msg.set(f"There has been a problem with encrypting column: {column_name}")
                        return False

                    # If field length is less than ciphertext length
                    # then update field type first then write the ciphertext
                    field_updated = self.update_field_type(column_name, cipher_length, error_msg)
                    
                    ciphertext_written =  self.write_to_table(sql_ct, error_msg) if field_updated else False

                    if ciphertext_written:
                        continue

                    error_msg.set(f"There has been a problem with encrypting column: {column_name}")
                    return False

                return False
            
            return True
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Decrypts the given column
    # Only performs the decryption of the ciphertexts
    # nothing more
    # + Generates the metadata
    # + For each column
    # ++ Gets the ciphertexts
    # ++ Create key of column name in dictionary
    # ++ Decrypts the data
    # ++ Appends the plaintext to the dictionary list
    def decrypt_table(self, error_msg):
        try:
            if len(self.all_columns) == 0:
                self.all_columns = self.get_all_columns(error_msg)
            
            plaintexts = {}
            hashed_metadata = self.generate_metadata("")

            for column in self.all_columns:
                column_name = column[0]

                # Skip column if it's a master foreign key column
                if self.is_master_foreign_column(column_name, error_msg):
                    continue

                PRIMARY_COLUMN = self.get_primary_key_column(error_msg) 
                ciphertexts = self.get_column_values(column_name, PRIMARY_COLUMN, error_msg)

                if ciphertexts:
                    if column_name not in plaintexts:
                        plaintexts[column_name] = []

                    for i in range(len(ciphertexts)):
                        ciphertext = ciphertexts[i][0]
                        plaintext = aes_encryptor.decrypt(ciphertext, error_msg)
                        plaintext = None if plaintext == 'None' else plaintext
                        plaintexts[column_name].append(plaintext)

            return plaintexts, hashed_metadata
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None, None
