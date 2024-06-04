from app.operation.cryptography.tle import Table_Encrypter
from app.operation.cryptography.cle import Column_Encrypter
from app.operation.cryptography.rle import Row_Encrypter
from app.operation.cryptography.cele import Cell_Encrypter
from app.operation.ekms_api import EKMS_API
from app.db.database import Table_Encryption_Model

import app.operation.db_password as db_password
import app.db.db_columns as db_columns
import app.operation.cryptography.ecc as ecc

class Table_View():

    def __init__(self, db_data_pack, table_name):
        self.db_data_pack = db_data_pack
        self.HOST = db_data_pack[0]
        self.DB_NAME = db_data_pack[1]
        self.DB_NICK = db_data_pack[2]
        self.USERNAME = db_data_pack[3]
        self.KEY_ROTATION_INTERVAL = db_data_pack[4]
        self.TABLE_NAME = table_name

        self.encryption_data = 0
        
        self.TABLE_ENCRYPTER = Table_Encrypter(db_data_pack, table_name)
        self.COLUMN_ENCRYPTER = Column_Encrypter(db_data_pack, table_name)
        self.ROW_ENCRYPTER = Row_Encrypter(db_data_pack, table_name)
        self.CELL_ENCRYPTER = Cell_Encrypter(db_data_pack, table_name)

    ## On -> no TLE implemented
    # Off -> TLE active
    def is_tle_enabled(self, error_msg):
        TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
        self.encryption_data = TABLE_ENC_MODEL.select_encryption_data(self.HOST, self.DB_NAME, self.TABLE_NAME)
        return True if self.encryption_data and '0' in [data[0] for data in self.encryption_data] else False

    ## Returns a dictionary of all columns and whether they
    # are encrypted - if in encryption data fetched from
    # cbdb database (seperate by ; as there may be multiple columns) 
    # and models match
    def gen_column_view(self, error_msg):
        password = db_password.get_password(self.HOST, self.DB_NAME, self.DB_NICK, error_msg)
        """ make self pass to each encryption class if blank then they fetch themselves otheruse use it """
        all_columns = db_columns.get_all_columns(self.HOST, self.DB_NAME, self.USERNAME, password, self.TABLE_NAME, error_msg)

        columns = {}

        if len(all_columns) > 0:
            # "<column>":<is_encrypted>
            for column in all_columns:
                column = column[0]
                is_encrypted = 'N'

                if self.encryption_data:
                    for data in self.encryption_data:
                        model = int(data[0])
                        detail = data[1]
                        is_encrypted = 'Y' if model == 1 and self.COLUMN_ENCRYPTER.exact_search(column, detail, ";") else 'N'

                        if is_encrypted == 'Y':
                            break

                columns[column] = is_encrypted

        return columns

    ## Returns the rows under the primary column of
    # a table by calling the functions in db_encryption level
    def get_primary_rows(self, error_msg):
        try:
            primary_column = self.COLUMN_ENCRYPTER.get_primary_key_column(error_msg)
            return self.COLUMN_ENCRYPTER.get_column_values(primary_column, primary_column, error_msg) if primary_column else []
        except Exception:
            error_msg.set("Fetching the rows has failed unexpectedly. Please try again later")
            return []

    ## Returns a dictionary of all rows and whether they
    # are encrypted - if in encryption data fetched from
    # cbdb database (seperate by ; as there may be multiple rows)
    # and if models match
    def gen_row_view(self, error_msg):
        """ Alter function, return both the column name and results make self and get use of it everywhere """
        all_rows = self.get_primary_rows(error_msg)

        rows = {}

        if len(all_rows) > 0:
            # "<row>":<is_encrypted>
            for row in all_rows:
                row = str(row[0])

                is_encrypted = 'N'

                if self.encryption_data:
                    for data in self.encryption_data:
                        model = int(data[0])
                        detail = data[1]
                        is_encrypted = 'Y' if model == 2 and self.COLUMN_ENCRYPTER.exact_search(row, detail, ';') else 'N'

                        if is_encrypted == 'Y':
                            break
                
                # Row width fix when encrypted
                row = row[:50] if len(row) > 50 else row

                rows[row] = is_encrypted
        
        return rows

    ## Returns a list of cell identifiers if models match
    # 
    def gen_cell_view(self, error_msg):
        return [item for data in self.encryption_data if int(data[0]) == 3 for item in data[1].split(";")]

    ## Checks if the new encryption is compatible with the hierarchy rules
    # If the encryption is CeLE then it checks if the new columns
    # are affected
    def check_encryption_hierarchy(self, new_model, identifier, error_msg):
        TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
        enc_models = TABLE_ENC_MODEL.select_encryption_data(self.HOST, self.DB_NAME, self.TABLE_NAME)

        decision_matrix = [
            # TLE, CLE, RLE, CeLE, NA
            ['TLE is already implemented', 'Y', 'Y', 'Y', 'Y'], # TLE
            ['Encryption hierarchy violation', 'Y', 'Y', 'Y', 'Y'], # CLE
            ['Encryption hierarchy violation', 'Encryption hierarchy violation', 'Y', 'Y', 'Y'], # RLE
            ['Encryption hierarchy violation', 'Encryption hierarchy violation', 'Encryption hierarchy violation', 'Y', 'Y']  # CeLE
        ]

        action = True if len(enc_models) == 0 else False

        for enc_model in enc_models:
            model = int(enc_model[0])

            detail = enc_model[1]
            detail = detail.split(";") if ';' in detail else [detail]

            decision = decision_matrix[new_model][model]

            if decision != 'Y' and new_model == 3 and model != 0:

                for item in identifier:
                    if model == 1:
                        new_detail = item.split(":")[0]
                    elif model == 2:
                        new_detail = item.split(":")[1]

                    matches = any(new_detail == d for d in detail)
                    action = not matches

                    if action != True:
                        break
            
            action = True if decision == 'Y' or action == True else decision

            if action != True and type(action) is str:
                break

        return action

    ## Calls the encryption function and updates the cbdb
    # database if passes the hierarchy check
    def encrypt_table(self, users, error_msg):
        can_encrypt = self.check_encryption_hierarchy(0, "", error_msg)

        if can_encrypt != True:
            error_msg.set(can_encrypt)
            return False

        table_encrypted = self.TABLE_ENCRYPTER.encrypt_table(users, error_msg)

        return self.TABLE_ENCRYPTER.add_table_enc_db("", "0", error_msg) if table_encrypted else False

    ## Calls the encryption function on the given column and updates
    # the cbdb database if passes the hierarchy check
    def encrypt_column(self, column, users, error_msg):
        can_encrypt = self.check_encryption_hierarchy(1, column, error_msg)

        if can_encrypt != True:
            error_msg.set(can_encrypt)
            return False

        column_encrypted = self.COLUMN_ENCRYPTER.encrypt_column(column, users, error_msg)

        return self.COLUMN_ENCRYPTER.add_table_enc_db(column, "1", error_msg) if column_encrypted else False

    ## Calls the encryption function on the given row id and updates
    # the cbdb database if passes the hierarchy check
    def encrypt_row(self, row, users, error_msg):
        can_encrypt = self.check_encryption_hierarchy(2, row, error_msg)

        if can_encrypt != True:
            error_msg.set(can_encrypt)
            return False

        row_encrypted = self.ROW_ENCRYPTER.encrypt_row(row, users, error_msg)

        return self.ROW_ENCRYPTER.add_table_enc_db(str(row), "2", error_msg) if row_encrypted else False

    ## Calls the get cells function in db encryption level
    #
    def get_cells(self, cell_inputs, error_msg):
        return self.CELL_ENCRYPTER.get_cells(cell_inputs, error_msg)

    ## Calls the cell preview function in db encryption level
    #
    def generate_cell_preview(self, error_msg):
        cell_preview_generated = self.CELL_ENCRYPTER.cells_preview(error_msg)
        return self.CELL_ENCRYPTER.results if cell_preview_generated else []

    ## Calls the encrypt cells function in db encryption level and
    # updates the cbdb database if passes the hierarchy check
    def encrypt_cells(self, error_msg):
        can_encrypt = self.check_encryption_hierarchy(3, self.CELL_ENCRYPTER.new_final_cells, error_msg)

        if can_encrypt != True:
            error_msg.set(can_encrypt)
            return False

        cells_encrypted = self.CELL_ENCRYPTER.encrypt_cells(error_msg)
        return self.CELL_ENCRYPTER.add_table_enc_db(self.CELL_ENCRYPTER.new_final_cells, "3", error_msg) if cells_encrypted else False

    ## Checks if the column in encryption removal is used in any other encryption
    # If yes then restore is false
    # If no then restore the column
    def check_field_update(self, column, cur_model, identifier, error_msg):
        TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
        enc_models = TABLE_ENC_MODEL.select_encryption_data(self.HOST, self.DB_NAME, self.TABLE_NAME)

        update = True

        for enc_model in enc_models:
            model = int(enc_model[0])
            detail = enc_model[1]
            detail = detail.split(";") if ';' in detail else detail
            detail = [detail] if type(detail) is not list else detail

            if model == 2 and cur_model == 2:
                # remove itself
                if str(identifier) in detail:
                    continue
            elif model == 2:
                return False
            
            new_detail = []

            if model == 3:
                for item in detail:
                    item = item.split(":")[0] if ':' in item else item
                    new_detail.append(item)
            
            matches = any(column == d for d in new_detail)

            update = not matches

            if not update:
                break
        
        return update

    ## Removes the encryption of the given model and identifier
    # + Decrypts the data
    # + Deletes the access control rules
    # + Gets the old data type and length
    # + Gets the current length
    # + Restores the old field type and any constraints
    # ++ For CeLE - if there are no other cells encrypted under that column
    # ++ For RLE - if there are no other rows encrypted
    # + Updates the table with the decrypted data
    # + Deletes the info on cbdb database
    # + Deletes the encryption key
    def remove_encryption(self, model, identifier, error_msg):
        
        """ Many repetitive blocks - make them common """

        ekms = EKMS_API(error_msg)

        if model == '0':
            # identifier = table name
            plaintexts, hashed_metadata = self.TABLE_ENCRYPTER.decrypt_table(error_msg)

            if plaintexts is not None and len(plaintexts) > 0 and hashed_metadata is not None:
                PRIMARY_COLUMN = self.TABLE_ENCRYPTER.get_primary_key_column(error_msg)
                primary_column_results = self.TABLE_ENCRYPTER.get_column_values(PRIMARY_COLUMN, PRIMARY_COLUMN, error_msg)

                if PRIMARY_COLUMN and len(primary_column_results) > 0:                   
                    # Moves the primary key column's data to last
                    # otherwise write function will fail
                    if PRIMARY_COLUMN in plaintexts:
                        plaintexts[PRIMARY_COLUMN] = plaintexts.pop(PRIMARY_COLUMN)

                    hashed_metadata = self.TABLE_ENCRYPTER.generate_metadata("")
                    key_id = ekms.get_key_id(hashed_metadata)

                    ac_rules_deleted = self.TABLE_ENCRYPTER.access_control.delete_ac_rules(key_id, error_msg)

                    if not ac_rules_deleted:
                        return False

                    for index, (key, value) in enumerate(plaintexts.items()):
                        old_data = self.TABLE_ENCRYPTER.get_old_field_data(key, error_msg)

                        old_data_type = old_data[0]
                        old_data_length = old_data[1]
                        old_data_length = int(old_data_length) if old_data_length else 0

                        # Generate a list of stored old constraint data
                        # by iterating them (index: [2,last elem])
                        stored_constraints = [old_data[i] for i in range(2, len(old_data))]

                        current_data = self.COLUMN_ENCRYPTER.get_field_type(key, error_msg)
                        current_data_length = current_data[1]

                        sql_pt = []

                        for i in range(len(value)):
                            if value[i] is not None:
                                sql_pt.append(f"UPDATE {self.TABLE_NAME} SET {key} = '{value[i]}' WHERE {PRIMARY_COLUMN} = '{primary_column_results[i][0]}'")
                            else:
                                sql_pt.append(f"UPDATE {self.TABLE_NAME} SET {key} = NULL WHERE {PRIMARY_COLUMN} = '{primary_column_results[i][0]}'")

                        plaintext_written = False
                        field_type_restored = False

                        restore_field_type = self.check_field_update(key, 0, "", error_msg)

                        # If old field type is VARCHAR and its length is greater than ciphertext length
                        # then restore the old field type and then write the plaintext
                        if old_data_type.startswith("varchar") and old_data_length > current_data_length:
                            field_type_restored = self.COLUMN_ENCRYPTER.restore_field_type(key, old_data_type, stored_constraints, error_msg) if restore_field_type else True

                            plaintext_written = self.COLUMN_ENCRYPTER.write_to_table(sql_pt, error_msg)

                        # If old field length is less than ciphertext length
                        # then write plaintext and then restore the old field type
                        else:
                            plaintext_written = self.COLUMN_ENCRYPTER.write_to_table(sql_pt, error_msg)

                            field_type_restored = self.COLUMN_ENCRYPTER.restore_field_type(key, old_data_type, stored_constraints, error_msg) if restore_field_type else True
                    
                    cbdb_updated = self.COLUMN_ENCRYPTER.remove_table_enc_db("0", "", error_msg)

                    """ change if logic delete if cbdb updated execute it if plain and field - Apply all """
                    enc_keys_deleted = ekms.delete_key_pair(hashed_metadata) if plaintext_written and field_type_restored and cbdb_updated else False

                    return ecc.delete_key_pair(hashed_metadata, error_msg) if enc_keys_deleted else False

        elif model == '1':
            # identifier = column name
            plaintexts, hashed_metadata = self.COLUMN_ENCRYPTER.decrypt_column(identifier, error_msg)

            if plaintexts is not None and len(plaintexts) > 0 and hashed_metadata is not None:
                old_data = self.COLUMN_ENCRYPTER.get_old_field_data(identifier, error_msg)
                old_data_type = old_data[0]
                old_data_length = old_data[1]
                old_data_length = int(old_data_length) if old_data_length else 0

                # Generate a list of stored old constraint data
                # by iterating them (index: [2,last elem])
                stored_constraints = [old_data[i] for i in range(2, len(old_data))]

                current_data = self.COLUMN_ENCRYPTER.get_field_type(identifier, error_msg)
                current_data_length = current_data[1]

                PRIMARY_COLUMN = self.COLUMN_ENCRYPTER.get_primary_key_column(error_msg)
                primary_column_results = self.COLUMN_ENCRYPTER.get_column_values(PRIMARY_COLUMN, PRIMARY_COLUMN, error_msg)
                
                if any(item is None for item in [old_data, current_data, PRIMARY_COLUMN, primary_column_results]):
                    return False

                hashed_metadata = self.TABLE_ENCRYPTER.generate_metadata(identifier)
                key_id = ekms.get_key_id(hashed_metadata)

                ac_rules_deleted = self.TABLE_ENCRYPTER.access_control.delete_ac_rules(key_id, error_msg)

                if not ac_rules_deleted:
                    return False

                sql_pt = []

                for i in range(len(plaintexts)):
                    if plaintexts[i] is not None:
                        sql_pt.append(f"UPDATE {self.TABLE_NAME} SET {identifier} = '{plaintexts[i]}' WHERE {PRIMARY_COLUMN} = '{primary_column_results[i][0]}'")
                    else:
                        sql_pt.append(f"UPDATE {self.TABLE_NAME} SET {identifier} = NULL WHERE {PRIMARY_COLUMN} = '{primary_column_results[i][0]}'")

                plaintext_written = False
                field_type_restored = False

                cbdb_updated = self.COLUMN_ENCRYPTER.remove_table_enc_db("1", identifier, error_msg)

                if not cbdb_updated:
                    return False

                restore_field_type = self.check_field_update(identifier, 1, identifier, error_msg)
                
                # If old field type is VARCHAR and its length is greater than ciphertext length
                # then restore the old field type and then write the plaintext
                if old_data_type.startswith("varchar") and old_data_length > current_data_length:
                    field_type_restored = self.COLUMN_ENCRYPTER.restore_field_type(identifier, old_data_type, stored_constraints, error_msg) if restore_field_type else True

                    plaintext_written = self.COLUMN_ENCRYPTER.write_to_table(sql_pt, error_msg)

                # If old field length is less than ciphertext length
                # then write plaintext and then restore the old field type
                else:
                    plaintext_written = self.COLUMN_ENCRYPTER.write_to_table(sql_pt, error_msg)

                    field_type_restored = self.COLUMN_ENCRYPTER.restore_field_type(identifier, old_data_type, stored_constraints, error_msg) if restore_field_type else True

                enc_keys_deleted = ekms.delete_key_pair(hashed_metadata) if plaintext_written and field_type_restored else False

                return ecc.delete_key_pair(hashed_metadata, error_msg) if enc_keys_deleted else False

        elif model == '2':
            # identifier = primary column value of the row
            plaintexts, hashed_metadata = self.ROW_ENCRYPTER.decrypt_row(identifier, error_msg)

            restore_field_type = True

            if plaintexts is not None and len(plaintexts) > 0 and hashed_metadata is not None:
                all_columns = self.ROW_ENCRYPTER.get_all_columns(error_msg)
                tmp_prim_key = (self.ROW_ENCRYPTER.TABLE_PRIMARY_KEY,)
                all_columns.remove(tmp_prim_key)

                plaintext_written = False
                field_type_restored = False

                hashed_metadata = self.TABLE_ENCRYPTER.generate_metadata(identifier)
                key_id = ekms.get_key_id(hashed_metadata)

                ac_rules_deleted = self.TABLE_ENCRYPTER.access_control.delete_ac_rules(key_id, error_msg)

                if not ac_rules_deleted:
                    return False

                for i in range(len(all_columns)):
                    column_name = all_columns[i][0]
                    plaintext = plaintexts[i]
                    
                    old_data = self.ROW_ENCRYPTER.get_old_field_data(column_name, error_msg)
                    old_data_type = old_data[0]
                    old_data_length = old_data[1]
                    old_data_length = int(old_data_length) if old_data_length else 0

                    # Generate a list of stored old constraint data
                    # by iterating them (index: [2,last elem])
                    stored_constraints = [old_data[i] for i in range(2, len(old_data))]

                    current_data = self.ROW_ENCRYPTER.get_field_type(column_name, error_msg)
                    current_data_length = current_data[1]

                    if any(item is None for item in [old_data, current_data]):
                        return False

                    if plaintext is not None:
                        sql_pt = [f"UPDATE {self.TABLE_NAME} SET {column_name} = '{plaintext}' WHERE {self.ROW_ENCRYPTER.TABLE_PRIMARY_KEY} = '{identifier}'"]
                    else:
                        sql_pt = [f"UPDATE {self.TABLE_NAME} SET {column_name} = NULL WHERE {self.ROW_ENCRYPTER.TABLE_PRIMARY_KEY} = '{identifier}'"]

                    restore = self.check_field_update(column_name, 2, identifier, error_msg)

                    # If old field type is VARCHAR and its length is greater than ciphertext length
                    # then restore the old field type and then write the plaintext
                    if old_data_type.startswith("varchar") and old_data_length > current_data_length:
                        field_type_restored = self.ROW_ENCRYPTER.restore_field_type(column_name, old_data_type, stored_constraints, error_msg) if restore else True

                        plaintext_written = self.ROW_ENCRYPTER.write_to_table(sql_pt, error_msg) if field_type_restored else False

                    # If old field length is less than ciphertext length
                    # then write plaintext and then restore the old field type
                    else:
                        plaintext_written = self.ROW_ENCRYPTER.write_to_table(sql_pt, error_msg)

                        field_type_restored = self.ROW_ENCRYPTER.restore_field_type(column_name, old_data_type, stored_constraints, error_msg) if restore else True

                cbdb_updated = self.ROW_ENCRYPTER.remove_table_enc_db("2", identifier, error_msg)

                enc_keys_deleted = ekms.delete_key_pair(hashed_metadata) if plaintext_written and field_type_restored and cbdb_updated else False

                return ecc.delete_key_pair(hashed_metadata, error_msg) if enc_keys_deleted else False

        elif model == '3':
            # identifier = cell identifier
            plaintext, hashed_metadata = self.CELL_ENCRYPTER.decrypt_cell(identifier, error_msg)

            restore_field_type = True

            if plaintext != "" and hashed_metadata is not None:
                column = identifier.split(":")[0]
                primary_value = identifier.split(":")[1]

                old_data = self.CELL_ENCRYPTER.get_old_field_data(column, error_msg)

                old_data_type = old_data[0]
                old_data_length = old_data[1]
                old_data_length = int(old_data_length) if old_data_length else 0

                # Generate a list of stored old constraint data
                # by iterating them (index: [2,last elem])
                stored_constraints = [old_data[i] for i in range(2, len(old_data))]

                current_data = self.CELL_ENCRYPTER.get_field_type(column, error_msg)
                current_data_length = current_data[1]

                TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
                stored_detail = TABLE_ENC_MODEL.get_detail(self.HOST, self.DB_NAME, self.TABLE_NAME, "3")
                stored_detail = stored_detail[0]

                if any(item is None for item in [old_data, current_data, stored_detail]):
                    return False

                hashed_metadata = self.TABLE_ENCRYPTER.generate_metadata(identifier)
                key_id = ekms.get_key_id(hashed_metadata)

                ac_rules_deleted = self.TABLE_ENCRYPTER.access_control.delete_ac_rules(key_id, error_msg)

                if not ac_rules_deleted:
                    return False
                
                # If there are multiple cells encrypted
                ## Remove the current one from the list
                ## Join remanining elements with : to be splitted
                # later to get a list of columns and row ids
                ## Check if the to be decrypted cell's column
                # is present in the remainings
                ## Restore old field type if not
                if ";" in stored_detail:
                    stored_detail_list = stored_detail.split(";")
                    stored_detail_list.remove(identifier)
                    tmp = ":".join(stored_detail_list)
                    new_stored_detail_list = tmp.split(":")
                    new_stored_detail = ";".join(new_stored_detail_list)

                    column_present = self.CELL_ENCRYPTER.exact_search(column, new_stored_detail, ";")

                    restore_field_type = False if column_present else True

                PRIMARY_COLUMN = self.CELL_ENCRYPTER.get_primary_key_column(error_msg)

                if plaintext is not None:
                    sql_pt = [f"UPDATE {self.TABLE_NAME} SET {column} = '{plaintext}' WHERE {PRIMARY_COLUMN} = '{primary_value}'"]
                else:
                    sql_pt = [f"UPDATE {self.TABLE_NAME} SET {column} = NULL WHERE {PRIMARY_COLUMN} = '{primary_value}'"]

                plaintext_written = False
                field_type_restored = False

                # If old field type is VARCHAR and its length is greater than ciphertext length
                # then restore the old field type and then write the plaintext
                if old_data_type.startswith("varchar") and old_data_length > current_data_length:
                    field_type_restored = self.CELL_ENCRYPTER.restore_field_type(column, old_data_type, stored_constraints, error_msg) if restore_field_type else True

                    plaintext_written = self.CELL_ENCRYPTER.write_to_table(sql_pt, error_msg)

                # If old field length is less than ciphertext length
                # then write plaintext and then restore the old field type
                else:
                    plaintext_written = self.CELL_ENCRYPTER.write_to_table(sql_pt, error_msg)

                    field_type_restored = self.CELL_ENCRYPTER.restore_field_type(column, old_data_type, stored_constraints, error_msg) if restore_field_type else True

                cbdb_updated = self.CELL_ENCRYPTER.remove_table_enc_db("3", identifier, error_msg)

                enc_keys_deleted = ekms.delete_key_pair(hashed_metadata) if plaintext_written and field_type_restored and cbdb_updated else False

                return ecc.delete_key_pair(hashed_metadata, error_msg) if enc_keys_deleted else False

        return False
