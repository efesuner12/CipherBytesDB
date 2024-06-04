from flask import request
from flask_restful import Resource
from datetime import datetime

import re

from app.api.requests.authentication import Authentication

from app.operation.validation import Validater
from app.db.database import Connected_Databases, Users, Table_Encryption_Model
from app.operation.ekms_api import EKMS_API
from app.operation.access_control import Access_Control
from app.operation.cryptography.tle import Table_Encrypter
from app.operation.cryptography.cle import Column_Encrypter
from app.operation.cryptography.rle import Row_Encrypter
from app.operation.cryptography.cele import Cell_Encrypter

import app.db.db_connection as db_connection
import app.db.db_columns as db_columns

class Request_Handler(Resource):

    ## Creates a pattern list and validates the incoming request
    # Returns the matched pattern if any
    def validate_request(self, sql_request):
        # columns + table name + condition - capture entire condition (match all) by greedy matching
        select_pattern_1 = r"SELECT (.+?) FROM ([\w]+) WHERE (.+)"

        # columns - non-greedy to capture individually + table name
        select_pattern_2 = r"SELECT (.+?) FROM ([\w]+)"

        # Created with lazy evaluation - requests with WHERE will tend to fall into select_pattern_2 so WHERE patterns come before them
        pattern_list = [select_pattern_1, select_pattern_2]

        VALIDATER = Validater()
        matched_pattern_index = VALIDATER.valid_sql_request(pattern_list, sql_request)

        return pattern_list[matched_pattern_index] if matched_pattern_index is not None else None

    ## Gets the user ID and the key ID
    # and checks if the user is authorised to
    # access this key
    def authorise(self, metadata):
        cbdb_users = Users("")
        user_id = cbdb_users.get_user_id(self.HOST, self.DB_NAME, self.USERNAME)

        self.ekms = EKMS_API("")
        key_id = self.ekms.get_key_id(metadata)

        if user_id is not None and key_id is not None:
            access_control = Access_Control([self.HOST, self.DB_NAME], self.TABLE_NAME)

            return access_control.has_access(user_id, key_id, "")

        return False

    ## Creates the encryption classes
    # Key rotation interval is not used in any decryption operations - not required
    def create_enc_classes(self):
        db_data_pack = [self.HOST, self.DB_NAME, self.DB_NICK, self.USERNAME, ""]

        self.TABLE_DECRYPTOR = Table_Encrypter(db_data_pack, self.TABLE_NAME)
        self.COLUMN_DECRYPTOR = Column_Encrypter(db_data_pack, self.TABLE_NAME)
        self.ROW_DECRYPTOR = Row_Encrypter(db_data_pack, self.TABLE_NAME)
        self.CELL_DECRYPTOR = Cell_Encrypter(db_data_pack, self.TABLE_NAME)

    ## Converts a datetime object into string
    #
    def convert_datetime_to_str_nested(self, input_list):
        return [[item.strftime('%Y-%m-%d %H:%M:%S') if isinstance(item, datetime) else item for item in sublist] for sublist in input_list]

    ## Fetches the encrypted table data by executing the SQL request
    # and fetches all columns of the table and the rows in the table data
    def get_encrypted_data(self, sql_request):
        try:
            conn, my_cursor = db_connection.connect({"host": self.HOST, "database": self.DB_NAME, "user": self.USERNAME, "password": self.PASSWORD})

            my_cursor.execute(sql_request)
            table_data = my_cursor.fetchall()
            table_data = [list(t) for t in table_data]
            table_data = self.convert_datetime_to_str_nested(table_data)

            all_columns = db_columns.get_all_columns(self.HOST, self.DB_NAME, self.USERNAME, self.PASSWORD, self.TABLE_NAME, "")
            all_columns = [column[0] for column in all_columns]

            PRIMARY_COLUMN = self.TABLE_DECRYPTOR.get_primary_key_column("")
            primary_rows = self.TABLE_DECRYPTOR.get_column_values(PRIMARY_COLUMN, PRIMARY_COLUMN, "")
            primary_rows = [str(row[0]) for row in primary_rows]

            #all_rows = [str(data[0]) for data in table_data]

            return all_columns, primary_rows, table_data
        except Exception:
            return None, None

    ## Returns the columns and values given in the condition
    #
    def get_condition_details(self, conditions):
                
        columns = []
        values = []
        
        conditions_split = re.split(r'\s+(AND|OR)\s+', conditions, flags=re.IGNORECASE)
        
        for condition in conditions_split:
            col_val = re.split(r'=|IS', condition)

            if len(col_val) == 2:
                col = col_val[0].strip()
                val = col_val[1].strip()

                try:
                    val = int(val)
                except ValueError:
                    pass

                val = None if val == 'NULL' else val

                columns.append(col)
                values.append(val)
        
        return columns, values

    ## Converts column based JSON representation to
    # row-by-row format
    def convert_JSON_format(self, data):
        keys = list(data.keys())
        new_data = [[int(row[i]) if row[i] is not None and row[i].isdigit() else row[i] for i in range(len(row))] for row in zip(*(data[key] for key in keys))]
        new_data = sorted(new_data, key=lambda x: x[0])

        return new_data

    ## Handles the incoming SQL request
    # + Validates the request
    # + Gets the columns from the request
    # + Gets the table name from the request
    # + Gets the conditions from the request if there are any
    # + Creates the encryption classes
    # + Gets the encryption models
    # ++ Return 404 Not found if none
    # + Gets all columns, rows and table data
    # + Sets columns to all columns if it's *
    # + Handles encryption models individually
    def handle_request(self, sql_request):
        try:
            matched_pattern = self.validate_request(sql_request)

            if not matched_pattern:
                return 'Not a valid SQL request', 400
            
            conn = None

            match = re.search(matched_pattern, sql_request, re.IGNORECASE)

            columns_str = match.group(1)
            columns = [col.strip() for col in columns_str.split(',')]

            self.TABLE_NAME = match.group(2)

            conditions = match.group(3) if "WHERE" in matched_pattern else None

            self.create_enc_classes()

            TABLE_ENC_MODEL = Table_Encryption_Model("")
            enc_models = TABLE_ENC_MODEL.select_encryption_data(self.HOST, self.DB_NAME, self.TABLE_NAME)

            if len(enc_models) == 0:
                return f"Table '{self.TABLE_NAME}' is not encrypted", 404

            all_columns, all_rows, table_data = self.get_encrypted_data(sql_request)

            columns = all_columns if columns == ['*'] else columns

            modes = [int(model[0]) for model in enc_models]
            details = [detail for model in enc_models for detail in model[1].split(";")]

            if any(column in detail for detail in details for column in columns) or any(row in details for row in all_rows) or (0 in modes):
                
                # TLE
                if 0 in modes:
                    # Authorise
                    hashed_metadata = self.TABLE_DECRYPTOR.generate_metadata("")

                    authorised = self.authorise(hashed_metadata)

                    if not authorised:
                        return f"'{self.USERNAME}' has no authorisation", 401

                    # Decrypt
                    dec_data = self.TABLE_DECRYPTOR.decrypt_table("")[0]
                    new_dec_data = self.convert_JSON_format(dec_data)

                    row_filtered_data = [] if conditions is not None else new_dec_data

                    # Get the row conditions and filter down the decrypted data
                    # Has limitations
                    # In other models they will be auto handled
                    # in SQL execution and table data update
                    if conditions is not None:
                        condition_cols, condition_vals = self.get_condition_details(conditions)

                        column_nos = [all_columns.index(column) for column in condition_cols]

                        for i in range(len(new_dec_data)):
                            row = new_dec_data[i]

                            for column_no in column_nos:
                                if row[column_no] in condition_vals and row not in row_filtered_data:
                                    row_filtered_data.append(row)

                    column_filtered_data = []

                    # Filter down the decrypted data if specific columns are
                    # requested
                    # For all rows, get the requested columns by NO and append
                    # to the list
                    if columns != all_columns:
                        for row in row_filtered_data:
                            tmp = [] # for row-by-row representation

                            for column in columns:
                                column_no =  all_columns.index(column)
                                tmp.append(row[column_no])
                            
                            column_filtered_data.append(tmp)

                    table_data = column_filtered_data if len(column_filtered_data) > 0 else row_filtered_data

                # CLE
                # Get the encrypted columns
                # For all encrypted columns
                # if the column is requested
                # decrypt
                # 
                if 1 in modes:
                    cle_details = [model[1] if int(model[0]) == 1 else "" for model in enc_models]

                    for detail in cle_details:

                        if detail == "":
                            continue

                        encrypted_columns = detail.split(";")
                        
                        for column in encrypted_columns:

                            if column in columns:
                                # Authorise
                                hashed_metadata = self.COLUMN_DECRYPTOR.generate_metadata(column)

                                authorised = self.authorise(hashed_metadata)

                                if not authorised:
                                    return f"'{self.USERNAME}' has no authorisation", 401
                                
                                # Decrypt
                                dec_data = self.COLUMN_DECRYPTOR.decrypt_column(column, "")[0]

                                # Get index from columns as you might have specifics
                                # If all, order will be the same
                                column_no = columns.index(column)

                                for i in range(len(table_data)):
                                    row = table_data[i]

                                    if conditions is None:
                                        row[column_no] = dec_data[i]
                                    else:
                                        con_cols, con_vals = self.get_condition_details(conditions)

                                        for value in con_vals:
                                            row[column_no] = dec_data[int(value)-1]
                
                # RLE
                if 2 in modes:
                    rle_details = [model[1] if int(model[0]) == 2 else "" for model in enc_models]

                    for detail in rle_details:

                        if detail == "":
                            continue
                        
                        encrypted_rows = detail.split(";")

                        for row in encrypted_rows:

                            if row in all_rows:
                                # authorise
                                hashed_metadata = self.ROW_DECRYPTOR.generate_metadata(row)

                                authorised = self.authorise(hashed_metadata)

                                if not authorised:
                                    return f"'{self.USERNAME}' has no authorisation", 401
                                
                                dec_data = self.ROW_DECRYPTOR.decrypt_row(row, "")[0]

                                row_no = all_rows.index(row)
                                
                                if conditions is None:
                                    if columns == all_columns:
                                        table_data[row_no][1:] = dec_data
                                    else:
                                        # Table data might be filtered with specific columns
                                        # so we need to extract those from the decrypted data
                                        # which is the whole row
                                        for i in range(len(columns)):
                                            column_no = all_columns.index(columns[i])
                                            # decrement one as the decrypted data won't include
                                            # the primary key column
                                            table_data[row_no][i] = dec_data[column_no-1]
                                else:
                                    tmp = []

                                    for i in range(len(columns)):
                                        column_no = all_columns.index(columns[i])
                                        tmp.append(dec_data[column_no-1])

                                    table_data.append(tmp)

                # CeLE
                if 3 in modes:
                    cele_details = [model[1] if int(model[0]) == 3 else "" for model in enc_models]
                    cele_details = "".join(cele_details)

                    cell_identifiers = cele_details.split(";")

                    for cell_id in cell_identifiers:
                        column = cell_id.split(':')[0]
                        row = cell_id.split(':')[1]

                        # check if the encrypted row is in the desired dataset
                        if row not in all_rows:
                            continue

                        # authorise
                        hashed_metadata = self.CELL_DECRYPTOR.generate_metadata(cell_id)

                        authorised = self.authorise(hashed_metadata)

                        if not authorised:
                            return f"'{self.USERNAME}' has no authorisation", 401

                        dec_data = self.CELL_DECRYPTOR.decrypt_cell(cell_id, "")
                        dec_data = dec_data[0]

                        column_no = all_columns.index(column)

                        row_no = all_rows.index(row)

                        table_data[row_no][column_no] = dec_data

                return table_data, 200

            return f"Requested datasets are not encrypted or don't exist", 404
        except Exception:
            return 'Unexpected error', 500
        finally:
            if conn and conn.is_connected():
                conn.close()

    ## HTTP GET
    # + Gets the token
    # + Authenticates the token
    # + If fails (return type tuple), returns the error
    # set on the authentication level
    # + Configures the class
    # + 
    def get(self, sql_request):
        token = request.json.get('token')

        authenticator = Authentication()
        decoded = authenticator.validate_auth_token(token)

        # Error on authentication level
        if type(decoded) == tuple:
            return decoded

        # Configure the class
        self.HOST = decoded['host']
        self.DB_NAME = decoded['database']
        self.USERNAME = decoded['username']
        self.PASSWORD = decoded['password']

        CONN_DBS = Connected_Databases("")
        self.DB_NICK = CONN_DBS.get_database_nick(self.HOST, self.DB_NAME)

        dec_data = self.handle_request(sql_request)

        return dec_data
