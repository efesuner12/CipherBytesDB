from app.operation.cryptography.db_encryption import Database_Encrypter
from app.operation.access_control import Access_Control

import app.operation.cryptography.aes as aes_encryptor

## Implements Cell Level Encryption (CeLE)
#
class Cell_Encrypter(Database_Encrypter):

    def __init__(self, db_data_pack, table_name):
        # Inherits from Database_Encryptor - uses its variables and functions
        super().__init__(db_data_pack)

        self.CELL_ENC_MODEL = "3"
        self.TABLE_NAME = table_name
        self.TABLE_PRIMARY_KEY = ""

        self.final_cells = []
        self.new_final_cells = []
        self.results = []

        self.access_control = Access_Control(db_data_pack, table_name)

    ## Gets the cells to be encrypted
    # + Clears the lists
    # + Check if the cells are blank
    # + Validate cells input
    # + Check if the same encryption exists
    # ++ If None: error in check level - return False
    # ++ Raise an error appropiate to the status code
    # ++ If a list is returned and it's not empty - raise a warning
    # + If cells include a cell under the primary key column - stop encryption
    def get_cells(self, cells, error_msg):
        
        self.final_cells.clear()
        self.new_final_cells.clear()
        self.results.clear()

        if cells == "":
            error_msg.set("Please provide cells to encrypt")
            return False

        if not self.VALIDATOR.valid_cell_identifier(cells):
            error_msg.set("Please enter the cells in the right format")
            return False

        same_encryption_exists = self.has_same_encryption(self.CELL_ENC_MODEL, cells, error_msg)

        self.final_cells = cells.split(";")

        if same_encryption_exists == None:
            return False
        elif same_encryption_exists == 1:
            error_msg.set(f"An encryption on '{self.TABLE_NAME}' with the same model and detail already exists")
            return False
        elif same_encryption_exists == 2 or same_encryption_exists == []:
            error_msg.set(f"The cell(s) is already encrypted")
            return False
        elif type(same_encryption_exists) == list and len(same_encryption_exists) > 0:
            error_msg.set(f"Cells that are already encrypted were removed.\nThe operation will carry on without them")
            self.final_cells = same_encryption_exists

        self.TABLE_PRIMARY_KEY = self.get_primary_key_column(error_msg)

        if any(cell.split(":")[0] == self.TABLE_PRIMARY_KEY for cell in cells.split(";")):
            error_msg.set(f"Cells under the primary key column cannot be encrypted\nin this model")
            return False

        return True

    ## Fetches the value of the cells for a preview and confirmation
    # + Gets the primary key column name of the table as users are expected to provide the values
    # + Gets the value of the given cell under the given column and the given primary key value
    # ++ If there is no result - invalid cell
    # + Append the existing ones to the results list
    def cells_preview(self, error_msg):
        try:
            if not self.TABLE_PRIMARY_KEY:
                self.TABLE_PRIMARY_KEY = self.get_primary_key_column(error_msg)

            for cell in self.final_cells:
                column = cell.split(":")[0]
                primary_value = cell.split(":")[1]

                result = self.get_cell_value(column, primary_value, error_msg)

                if not result:
                    self.results.append(f"'{cell}' is not an existing cell. The operation will\ncarry on without it")
                    continue

                self.new_final_cells.append(cell)
                self.results.append(str(result[0]))
                
            return True
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Encrypts the given cell(s)
    # Performs the whole operation
    # + For each cell to be encrypted
    # ++ Skips if the value is a warning
    # ++ Generates the metadata
    # ++ Generates the secrets
    # ++ Encrypts the value
    # ++ Generates the SQL statement to update the table with the ciphertext for a bulk update
    # ++ Gets the current field type and length
    # ++ Gets the length of the ciphertext
    # ++ If current field type is varchar and its len is greater than the ciphertext's
    # +++ Updates the table with the ciphertext
    # +++ Updates the column data type
    # ++ Else
    # +++ Updates the column data type and writes the ciphertext
    # This is a strategy followed to avoid format and length errors
    # ++ In each iteration, continues if there are no errors else returns False
    def encrypt_cells(self, error_msg):

        try:
            sql_ct = []

            for i in range(len(self.new_final_cells)):

                if "is not an existing cell. The operation will carry on without it" in self.results[i]:
                    continue

                cell = self.new_final_cells[i]

                hashed_metadata = self.generate_metadata(cell)
                key, key_id = self.generate_enc_key(hashed_metadata, error_msg)
                nonce = self.generate_enc_nonce()

                ciphertext = aes_encryptor.encrypt(str(self.results[i]), hashed_metadata, key, nonce, error_msg)

                if ciphertext:
                    column = (cell).split(":")[0]
                    primary_value = (cell).split(":")[1]

                    sql_ct.append(f"UPDATE {self.TABLE_NAME} SET {column} = '{ciphertext}' WHERE {self.TABLE_PRIMARY_KEY} = '{primary_value}'")

                    current_field_type = self.get_field_type(column, error_msg)
                    field_type = current_field_type[0]

                    field_length = current_field_type[1]
                    field_length = int(field_length) if field_length else 0

                    cipher_length = len(ciphertext)
                    cipher_length = 64 if cipher_length < 64 else cipher_length
    
                    # If field type is VARCHAR and its length is greater than ciphertext length
                    # then write ciphertext then update the field type
                    if field_type == "varchar" and field_length > cipher_length:
                        ciphertext_written =  self.write_to_table(sql_ct, error_msg)

                        field_updated = self.update_field_type(column, cipher_length, error_msg) if ciphertext_written else False

                        if field_updated:
                            continue
                        
                        error_msg.set(f"There has been a problem with encrpting cell: {cell}")
                        return False

                    # If field length is less than ciphertext length
                    # then update field type first then write the ciphertext
                    field_updated = self.update_field_type(column, cipher_length, error_msg)

                    ciphertext_written = self.write_to_table(sql_ct, error_msg) if field_updated else False

                    if ciphertext_written:
                        continue
                    
                    error_msg.set(f"There has been a problem with encrpting cell: {cell}")
                    return False
                
                return False

            return True
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Decrypts the given cell
    # Only performs the decryption of the ciphertext
    # nothing more
    # + Gets the primary key column of the table
    # + Gets the ciphertext
    # + Decrypts the data
    def decrypt_cell(self, cell, error_msg):
        try:
            column = cell.split(":")[0]
            primary_value = cell.split(":")[1]

            plaintext = ""
            hashed_metadata = None

            if not self.TABLE_PRIMARY_KEY:
                self.TABLE_PRIMARY_KEY = self.get_primary_key_column(error_msg)

            ciphertext = self.get_cell_value(column, primary_value, error_msg)

            if ciphertext:
                ciphertext = ciphertext[0]

                hashed_metadata = self.generate_metadata(cell)
                plaintext = aes_encryptor.decrypt(ciphertext, error_msg)
                plaintext = None if plaintext == 'None' else plaintext

            return plaintext, hashed_metadata
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return "", None
