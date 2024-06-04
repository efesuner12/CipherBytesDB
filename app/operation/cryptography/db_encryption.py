import mysql.connector
import ast

from app.operation.validation import Validater
from app.db.database import Table_Encryption_Model, Encrypted_Column_Data
from app.operation.ekms_api import EKMS_API
from app.operation.access_control import Access_Control

import app.db.db_connection as db_connection
import app.db.db_columns as db_columns
import app.operation.db_password as db_password
import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor

## Is the parent encryptor and holds
# data that will be used across all child encryptors
class Database_Encrypter():

    def __init__(self, db_data_pack):
        self.HOST = db_data_pack[0]
        self.DB_NAME = db_data_pack[1]
        self.DB_NICK = db_data_pack[2]
        self.USERNAME = db_data_pack[3]
        self.KEY_ROTATION_INTERVAL = db_data_pack[4]

        self.conn = None
        self.my_cursor = None
        self.password = None

        self.VALIDATOR = Validater()

    ## Established a database connection with the given configs
    #
    def get_connection(self, error_msg):
        try:
            self.password = db_password.get_password(self.HOST, self.DB_NAME, self.DB_NICK, error_msg)
            self.conn, self.my_cursor = db_connection.connect({"host": self.HOST, "database": self.DB_NAME, "user": self.USERNAME, "password": self.password})
        except Exception:
            error_msg.set("Connecting has failed unexpectedly. Please try again later")

    ## Closes the MySQL connection
    #
    def close_connection(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()

    ## Generates the hashed metadata for all encryption models
    # AD being the additional data:
    # TLE: table name
    # CLE: column name
    # RLE: primary key
    # CeLE: cell id
    def generate_metadata(self, ad):
        metadata = f"{self.HOST}#{self.DB_NAME}#{self.DB_NICK}#{self.TABLE_NAME}"
        metadata += f"#{ad}" if ad != "" else ""
        return hasher.sha_512_hash(metadata)

    ## Returns the generated AES nonce
    #
    def generate_enc_nonce(self):
        nonce = aes_encryptor.generate_nonce()
        return nonce

    ## Returns the generated AES key and its ID
    #
    def generate_enc_key(self, metadata, error_msg):
        key = aes_encryptor.generate_key(metadata, self.KEY_ROTATION_INTERVAL, error_msg)
        
        ekms = EKMS_API(error_msg)
        key_id = ekms.get_key_id(metadata)

        return key, key_id

    ## Returns the values under the given column
    #
    def get_column_values(self, column_name, primary_key, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT {column_name} FROM {self.TABLE_NAME} ORDER BY {primary_key}")
            results = self.my_cursor.fetchall()

            return results
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the field type and its length of the given column
    #
    def get_field_type(self, column_name, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT DATA_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.DB_NAME}' AND TABLE_NAME = '{self.TABLE_NAME}' AND COLUMN_NAME = '{column_name}'")
            result = self.my_cursor.fetchone()

            return result
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the primary key column name of the table in operation
    #
    def get_primary_key_column(self, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_NAME = '{self.TABLE_NAME}' AND CONSTRAINT_NAME = 'PRIMARY'")
            result = self.my_cursor.fetchone()

            return result[0] if result else None
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the default and not null constraints' details
    #
    def get_basic_constraints(self, column_name, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT COLUMN_DEFAULT, IS_NULLABLE, EXTRA FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.DB_NAME}' and TABLE_NAME = '{self.TABLE_NAME}' AND COLUMN_NAME = '{column_name}'")
            stored_constrains = self.my_cursor.fetchone()

            return stored_constrains
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the next auto increment value of the table
    #
    def get_auto_inc_constraint(self, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SHOW TABLE STATUS LIKE '{self.TABLE_NAME}'")
            result = self.my_cursor.fetchone()

            return result[10]
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the check constraint details if it belongs to the given
    # column as the original query is done on the whole of the database
    def get_check_constraint(self, column_name, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT CONSTRAINT_NAME, CHECK_CLAUSE FROM INFORMATION_SCHEMA.CHECK_CONSTRAINTS WHERE CONSTRAINT_SCHEMA = '{self.DB_NAME}'")
            result = self.my_cursor.fetchone()
            
            if not result:
                return None

            tmp = result[1].replace('(', '')
            tmp = tmp.replace(')', '')
            splitted = tmp.split(" ")

            if len(splitted) == 0 or splitted[0] != f"`{column_name}`":
                return None

            constraint_name = result[0]

            return (constraint_name, splitted[1], splitted[2])
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Checks if the given column is a 'master' foreign key column
    # i.e. other tables' columns uses its values
    def is_master_foreign_column(self, column_name, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT CONSTRAINT_NAME, TABLE_NAME, COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE REFERENCED_TABLE_SCHEMA = '{self.DB_NAME}' AND REFERENCED_TABLE_NAME = '{self.TABLE_NAME}' AND REFERENCED_COLUMN_NAME = '{column_name}';")
            results = self.my_cursor.fetchall()

            return True if len(results) > 0 else False
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the foreign key constraint details of the given column
    #
    def get_foreign_key_constraint(self, column_name, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT CONSTRAINT_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.DB_NAME}' AND TABLE_NAME = '{self.TABLE_NAME}' AND COLUMN_NAME = '{column_name}' AND REFERENCED_TABLE_NAME IS NOT NULL AND REFERENCED_COLUMN_NAME IS NOT NULL")
            foreign_key_constraint = self.my_cursor.fetchone()

            return foreign_key_constraint
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the constraint name of the unique constraint of the given column
    # This SQL command has 2 parts: setting the column filter and the constraint name
    def get_unique_constraint(self, column_name, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = '{self.DB_NAME}' AND TABLE_NAME = '{self.TABLE_NAME}' AND CONSTRAINT_NAME IN (SELECT CONSTRAINT_NAME FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS WHERE CONSTRAINT_TYPE = 'UNIQUE' AND TABLE_SCHEMA = '{self.DB_NAME}' AND TABLE_NAME = '{self.TABLE_NAME}') AND COLUMN_NAME = '{column_name}'")
            unique_constraint = self.my_cursor.fetchone()

            return unique_constraint[0] if unique_constraint else None
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Fetches the constraint details,
    # drops them by creating a SQL command for each 
    # (default, not null, auto increment) will be dropped by changing the data type
    # in update_field_type anyway - no specific SQL generated
    # and returns them to be added into the database
    def drop_and_store_constraints(self, column_name, error_msg):
        try:
            stored_constrains = self.get_basic_constraints(column_name, error_msg)

            # Default 
            default_val = stored_constrains[0]

            # Not Null
            not_null = True if stored_constrains[1] == 'NO' else False

            # Auto increment
            auto_inc_val = self.get_auto_inc_constraint(error_msg) if "auto_increment" in stored_constrains else None
            
            # Check
            check_vals = self.get_check_constraint(column_name, error_msg)

            # Foreign Key
            foreign_key_vals = self.get_foreign_key_constraint(column_name, error_msg)

            # Unique
            unique_val = self.get_unique_constraint(column_name, error_msg)

            sql = []

            sql.append(f"ALTER TABLE {self.TABLE_NAME} DROP CHECK {check_vals[0]}") if check_vals else None

            sql.append(f"ALTER TABLE {self.TABLE_NAME} DROP FOREIGN KEY {foreign_key_vals[0]}") if foreign_key_vals else None

            sql.append(f"ALTER TABLE {self.TABLE_NAME} DROP INDEX {unique_val}") if unique_val else None

            constraints_dropped = self.write_to_table(sql, error_msg) if len(sql) > 0 else True

            return [default_val, auto_inc_val, str(not_null), check_vals, foreign_key_vals, unique_val] if constraints_dropped else []
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return []

    ## Updates the given column's data type to VARCHAR(l)
    # l being the max length of the ciphertexts
    # Adds the received constraint data to the database along with
    # the old data type and length
    def update_field_type(self, column_name, length, error_msg):
        try:
            constraints = self.drop_and_store_constraints(column_name, error_msg)

            if len(constraints) == 0:
                return False

            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT COLUMN_TYPE, CHARACTER_MAXIMUM_LENGTH FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '{self.DB_NAME}' AND TABLE_NAME = '{self.TABLE_NAME}' AND COLUMN_NAME = '{column_name}'")
            old_data_type = self.my_cursor.fetchone()

            self.my_cursor.execute(f"ALTER TABLE {self.TABLE_NAME} MODIFY COLUMN {column_name} VARCHAR({length})")
            self.conn.commit()

            ENC_COLUMN_DATA = Encrypted_Column_Data(error_msg)
            return ENC_COLUMN_DATA.add_data(self.HOST, self.DB_NAME, self.TABLE_NAME, column_name, old_data_type[0], old_data_type[1], constraints)
        except Exception:
            # 3780
            # 1451
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False
        finally:
            self.close_connection()

    ## Runs the SQL statements to insert the ciphertexts or plaintexts
    #
    def write_to_table(self, sql, error_msg):
        try:
            if len(sql) <= 0:
                return False

            self.get_connection(error_msg)

            for i in range(len(sql)):
                self.my_cursor.execute(sql[i])
            
            # Commiting all at once saves utter time
            self.conn.commit()
            
            return True
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False
        finally:
            self.close_connection()

    ## Adds the new detail to the 
    # Table Encryption Model table
    def add_table_enc_db(self, data, model, error_msg):
        
        if len(data) > 0 or model == '0':
            # if CeLE
            detail = ";".join(data) if model in ['3'] else data

            TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
            added = TABLE_ENC_MODEL.add_table_encryption(self.HOST, self.DB_NAME, self.TABLE_NAME, model, detail)

            return added

    ## Returns the values of the given row
    #
    def get_row_values(self, primary_value, error_msg):
        try:
            self.get_connection(error_msg)

            self.my_cursor.execute(f"SELECT * FROM {self.TABLE_NAME} WHERE {self.TABLE_PRIMARY_KEY} = '{primary_value}'")
            results = self.my_cursor.fetchall()

            return results
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False
        finally:
            self.close_connection()

    ## Calls the database columns class
    #
    def get_all_columns(self, error_msg):
        self.password = db_password.get_password(self.HOST, self.DB_NAME, self.DB_NICK, error_msg) if not self.password else self.password
        return db_columns.get_all_columns(self.HOST, self.DB_NAME, self.USERNAME, self.password, self.TABLE_NAME, error_msg)

    ## Returns if the whole of a search string matches to the stored string
    # in all of its elements
    def exact_search_all(self, search_string, stored_string, delimeter):
        return any(pair.strip() == search_string for pair in stored_string.split(delimeter))

    ## Returns if search string (individual str) matches any of the stored strings
    #
    def exact_search(self, search_string, stored_string, delimeter):
        for s in search_string.split(delimeter):
            for ss in stored_string.split(delimeter):
                if s == ss:
                    return True
        
        return False

    ## Compares the new detail with the stored detail in the database
    # + Gets the current detail stored in the database
    # + Returns status code 1 if new detail exactly matches the stored
    # + Returns status code 2 if the whole of the new detail matches a part of the stored
    # + Returns False if it doesn't
    # + Else returns a list of details that are not already stored
    # + Returns False if there are no detail stored in the database
    def has_same_encryption(self, model, detail, error_msg):
        try:
            TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
            stored_detail = TABLE_ENC_MODEL.get_detail(self.HOST, self.DB_NAME, self.TABLE_NAME, model)
            
            if stored_detail:
                stored_detail = stored_detail[0]

                if stored_detail == detail:
                    return 1
                elif self.exact_search_all(detail, stored_detail, ';'):
                    return 2
                elif not self.exact_search(detail, stored_detail, ';'):
                    return False

                return [str(cell) for cell in detail.split(";") if not self.exact_search(cell, stored_detail, ';')]

            return False
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Returns the cells under the given column with the given filter
    # and handles a specific error case
    def get_cell_value(self, column_name, primary_value, error_msg):
        try:
            self.get_connection(error_msg)

            # mind the self.TABLE_PRIMARY_KEY here!
            self.my_cursor.execute(f"SELECT {column_name} FROM {self.TABLE_NAME} WHERE {self.TABLE_PRIMARY_KEY} = '{primary_value}'")
            result = self.my_cursor.fetchone()

            return result
        except Exception as e:
            # Passing unknown column error as it will be
            # raised in cell preview regardless
            # no error message when returned to cell input page
            if e.errno == 1054:
                return None
            
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None
        finally:
            self.close_connection()

    ## Returns the old field data - type, length, constraints
    #
    def get_old_field_data(self, column_name, error_msg):
        ENC_COLUMN_DATA = Encrypted_Column_Data(error_msg)
        old_data_type = ENC_COLUMN_DATA.select_data(self.HOST, self.DB_NAME, self.TABLE_NAME, column_name)

        return old_data_type

    ## Restores the old field type and any constraints 
    # of the given column and deletes its information
    # from the database
    def restore_field_type(self, column_name, old_type, old_constraints, error_msg):
        try:
            base_sql_1 = f"ALTER TABLE {self.TABLE_NAME} MODIFY COLUMN {column_name} {old_type}"
            base_sql_2 = f"ALTER TABLE {self.TABLE_NAME} ADD CONSTRAINT "

            sql = []

            # 0 - Not null
            if old_constraints[2] is not None and old_constraints[2] == 'True':
                base_sql_1 += f" NOT NULL"

            # 1 - Default
            if old_constraints[0] is not None:
                base_sql_1 += f" DEFAULT {old_constraints[0]}"

            # 2 - Auto increment
            # Add constraint to the column
            # Set its custom value
            if old_constraints[1] is not None:
                base_sql_1 += f" AUTO_INCREMENT"
                sql.append(f"ALTER TABLE {self.TABLE_NAME} AUTO_INCREMENT={int(old_constraints[1])}")

            sql.append(base_sql_1)

            # Once the basic modifications are done with the data type
            # and basic constraints, rest will be added
            # otherwise they will fail

            # 3 - Check
            # Try converting the value to int in case it is else it's a string
            # Based on the operator string generate the SQL
            if old_constraints[3] is not None:
                check_data = ast.literal_eval(old_constraints[3])

                if check_data[1] == '=':
                    sql.append(base_sql_2 + f"{check_data[0]} CHECK ({column_name}={check_data[2]})")
                elif check_data[1] == '>':
                    sql.append(base_sql_2 + f"{check_data[0]} CHECK ({column_name}>{check_data[2]})")
                elif check_data[1] == '<':
                    sql.append(base_sql_2 + f"{check_data[0]} CHECK ({column_name}<{check_data[2]})")
                elif check_data[1] == '>=':
                    sql.append(base_sql_2 + f"{check_data[0]} CHECK ({column_name}>={check_data[2]})")
                elif check_data[1] == '<=':
                    sql.append(base_sql_2 + f"{check_data[0]} CHECK ({column_name}<={check_data[2]})")
                elif check_data[1] == '<>':
                    sql.append(base_sql_2 + f"{check_data[0]} CHECK ({column_name}<>{check_data[2]})")
            
            # 4 - Foreign key
            if old_constraints[4] is not None:
                foreign_data = ast.literal_eval(old_constraints[4])

                tmp_sql = base_sql_2 + f"{foreign_data[0]} FOREIGN KEY ({column_name}) REFERENCES {foreign_data[1]}({foreign_data[2]})"
                sql.append(tmp_sql)

            # 5 - Unique
            if old_constraints[5] is not None:
                tmp_sql = base_sql_2 + f"{old_constraints[5]} UNIQUE ({column_name})"
                sql.append(tmp_sql)

            restored = self.write_to_table(sql, error_msg)

            ENC_COLUMN_DATA = Encrypted_Column_Data(error_msg)
            return ENC_COLUMN_DATA.delete_data(self.HOST, self.DB_NAME, self.TABLE_NAME, column_name) if restored else False
        except Exception:
            error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Calls the remove encryption model function
    # in database level
    def remove_table_enc_db(self, model, detail, error_msg):
        TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
        return TABLE_ENC_MODEL.delete_table_encryption(self.HOST, self.DB_NAME, self.TABLE_NAME, model, detail)
