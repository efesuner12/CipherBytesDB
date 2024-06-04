from mysql.connector import IntegrityError

from app.db.cbdb_connection import DB_Connection
from app.operation.validation import Validater

class Admin_Database(DB_Connection):

    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()
        
        self.error_msg = error_msg
        self.VALIDATER = Validater()

    ## Checks if the given username exists
    # by selecting it from the admin table
    # if it's a valid username input
    def has_username(self, username):

        if not self.VALIDATER.valid_username(username):
            self.error_msg.set("Please enter a valid username")
            return None

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT username FROM admin WHERE username = '{username}'")
            results = DB_Connection.cbdb_cursor.fetchall()

            return True if results else False
        except Exception as e:
            # Handles an attribute error - db connection failed because
            # of incorrect password -> kdf: wrong key -> decryption failed
            if "'NoneType' object has no attribute 'execute'" in str(e):
                self.error_msg.set("Incorrect password")
            else:
                self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Selects the password hash of the given username
    # for login if username is valid
    # Another username validation check is done as a protection against
    # an individual call on this function
    def select_password(self, username):

        if not self.VALIDATER.valid_username(username):
            self.error_msg.set("Please enter a valid username")
            return 0

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT password FROM admin WHERE username = '{username}'")
            result = DB_Connection.cbdb_cursor.fetchone()

            return result
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return 0

class Connected_Databases(DB_Connection):

    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()

        self.error_msg = error_msg
        self.VALIDATER = Validater()

    ## Checks if there are connected databases
    # by counting the IDs
    def has_connected_dbs(self):

        try:
            DB_Connection.cbdb_cursor.execute("SELECT COUNT(id) FROM connected_dbs")
            result = DB_Connection.cbdb_cursor.fetchone()
            count = result[0]

            return count > 0
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Checks if the given connection already exists
    # if the host is valid
    def has_connection(self, host, db_name):
        
        if not self.VALIDATER.valid_host(host):
            self.error_msg.set("Please enter a valid host address")
            return None

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT host, db_name FROM connected_dbs WHERE host = '{host}' AND db_name = '{db_name}'")
            results = DB_Connection.cbdb_cursor.fetchall()

            return True if results else False
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Adds a new database connection
    # to the global connected_dbs table
    # Another host validation check is done as a protection against
    # an individual call on this function
    def add_new_connection(self, host, db_name, db_nick, username, password, key_rotation_interval):

        if not self.VALIDATER.valid_host(host):
            self.error_msg.set("Please enter a valid host address")
            return False
        
        if not self.VALIDATER.valid_username(username):
            self.error_msg.set("Please enter a valid username")
            return False

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            sql = "INSERT INTO connected_dbs (host, db_name, db_nickname, username, password, key_rotation_interval) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (host, db_name, db_nick, username, password, key_rotation_interval)

            DB_Connection.cbdb_cursor.execute(sql, val)
            DB_Connection.cbdb_conn.commit()

            return True
        except IntegrityError as e:
            # MySQL error code for duplicate entry
            if e.errno == 1062:
                error_msg = str(e.args[1]).split(": ")[1]
                self.error_msg.set(error_msg)
            else:
                self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            
            return False
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Returns the connected databases
    #
    def select_connected_databases(self):

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT host, db_name, username, db_nickname, key_rotation_interval FROM connected_dbs")
            results = DB_Connection.cbdb_cursor.fetchall()

            return results
        except Exception:
            self.error_msg.set("Fetching connections operation has\nfailed unexpectedly. Please try again later")
            return None

    ## Deletes the given database from the table
    # using the host and db name
    def delete_database(self, host, db_name):

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM connected_dbs WHERE host = '{host}' AND db_name = '{db_name}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Selects the encrypted password of the
    # given host and database name
    def select_password(self, host, db_name):

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT password FROM connected_dbs WHERE host = '{host}' AND db_name = '{db_name}'")
            result = DB_Connection.cbdb_cursor.fetchone()

            return result
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Updates the password of the given database
    #
    def update_password(self, host, db_name, new_password):
        
        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"UPDATE connected_dbs SET password = '{new_password}' WHERE host = '{host}' AND db_name = '{db_name}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False
    
    ## Updates the given configs of the database
    # by determining which are changed
    def update_database_connection(self, host, db_name, db_nick, username, key_rotation_var):

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        counter = 0

        try:
            sql = f"UPDATE connected_dbs SET "
            sql_final = f" WHERE host = '{host}' AND db_name = '{db_name}'"

            if db_nick:
                sql += f"db_nickname = '{db_nick}'"
                counter += 1
            if username:
                if counter > 0:
                    sql += f" , "
                sql += f"username = '{username}'"
                counter += 1
            if key_rotation_var:
                if counter > 0:
                    sql += f" , "
                sql += f"key_rotation_interval = '{key_rotation_var}'"
                counter += 1

            sql += sql_final

            DB_Connection.cbdb_cursor.execute(sql)
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Gets the nickname of the given database
    #
    def get_database_nick(self, host, db_name):
        
        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT db_nickname FROM connected_dbs WHERE host = '{host}' AND db_name = '{db_name}'")
            result = DB_Connection.cbdb_cursor.fetchone()

            return result[0]
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

class Users(DB_Connection):
    
    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()

        self.error_msg = error_msg

    ## Checks how many users there are with the given
    # host id and username
    def has_user(self, host, db_name, username):

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT COUNT(username) FROM users WHERE host_identifier = '{host}#{db_name}' AND username = '{username}'")
            result = DB_Connection.cbdb_cursor.fetchone()

            return result[0] > 0
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Adds the final users into db by
    # creating a sql command by iterating through the dictionary
    # If the user already exists then continues with the next
    def add_users(self, host, db_name, users):

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            sql = "INSERT INTO users (host_identifier, username, user_privilage) VALUES "

            # key: username
            # value: role
            # add a comma (,) if it's not the last iteration - no comma at the end
            for index, (key,value) in enumerate(users.items()):

                if self.has_user(host, db_name, key):
                    continue

                sub_sql = f"('{host}#{db_name}', '{key}', '{value}')"

                if not (index == len(users) -1):
                    sub_sql += ", "

                sql += sub_sql

            DB_Connection.cbdb_cursor.execute(sql)
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes the users of the given host_identifier
    #
    def delete_users(self, host, db_name):

        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM users WHERE host_identifier = '{host}#{db_name}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Gets the ID of the given user of a
    # particular host and database
    def get_user_id(self, host, db_name, username):

        # localhost and 127.0.0.1 are the same
        host = "localhost" if host == "127.0.0.1" else host

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT id FROM users WHERE host_identifier = '{host}#{db_name}' AND username = '{username}'")
            result = DB_Connection.cbdb_cursor.fetchone()

            return result[0]
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

class Table_Encryption_Model(DB_Connection):
    
    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()

        self.error_msg = error_msg

    ## Selects the tables that are encrypted and
    # their encryption models of a given host_identifier
    def select_table_encryption(self, host, db_name):

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT table_name, encryption_model FROM table_encryption_model WHERE host_identifier = '{host}#{db_name}'")
            results = DB_Connection.cbdb_cursor.fetchall()

            return results
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Gets the stored detail of the given host identifier,
    # table and model
    def get_detail(self, host, db_name, table_name, model):

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT detail FROM table_encryption_model WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND encryption_model = '{model}'")
            detail = DB_Connection.cbdb_cursor.fetchone()

            return detail
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Checks if the given encryption model against
    # the given host identifier and table exists
    def has_encryption(self, host, db_name, table_name, model):

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT * FROM table_encryption_model WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND encryption_model = '{model}'")
            results = DB_Connection.cbdb_cursor.fetchall()

            return True if results else False
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Updates the encryption detail of the given host identifier,
    # table and model
    def update_detail(self, host, db_name, table_name, model, new_detail):

        try:
            DB_Connection.cbdb_cursor.execute(f"UPDATE table_encryption_model SET detail = '{new_detail}' WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND encryption_model = '{model}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Adds the table encryption model and the details
    # to the database and checks if the encryption exists
    def add_table_encryption(self, host, db_name, table_name, model, detail):

        try:
            encryption_exists = self.has_encryption(host, db_name, table_name, model)

            # Error in has_encryption level
            if encryption_exists == None:
                return False
            elif encryption_exists:
                existing_detail = self.get_detail(host, db_name, table_name, model)

                if not existing_detail:
                    return False
                
                new_detail = existing_detail[0] + f";{detail}"

                updated = self.update_detail(host, db_name, table_name, model, new_detail)

                return True if updated else False

            sql = "INSERT INTO table_encryption_model (host_identifier, table_name, encryption_model, detail) VALUES (%s, %s, %s, %s)"
            val = (f"{host}#{db_name}", table_name, model, detail)

            DB_Connection.cbdb_cursor.execute(sql, val)
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes the encryption model of a given table and model
    #
    def delete_table_encryption(self, host, db_name, table_name, model, detail):

        try:
            stored_detail = self.get_detail(host, db_name, table_name, model)

            if stored_detail:
                stored_detail = stored_detail[0]

                if ';' in stored_detail:
                    splitted = stored_detail.split(";")
                    splitted.remove(detail)
                    new_detail = ";".join(splitted)
                    
                    return self.update_detail(host, db_name, table_name, model, new_detail)   
                
                DB_Connection.cbdb_cursor.execute(f"DELETE FROM table_encryption_model WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND encryption_model = '{model}' AND detail = '{detail}'")
                DB_Connection.cbdb_conn.commit()

                return True

            return False
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes all encryption models of a given host identifier
    #
    def delete_table_encryption_all(self, host, db_name):

        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM table_encryption_model WHERE host_identifier = '{host}#{db_name}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Selects the encryption model and the detail of a 
    # give table 
    def select_encryption_data(self, host, db_name, table_name):

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT encryption_model, detail FROM table_encryption_model WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}'")
            results = DB_Connection.cbdb_cursor.fetchall()

            return results
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

class Encrypted_Column_Data(DB_Connection):

    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()

        self.error_msg = error_msg

    ## Selects the encrypted column data of the given host
    # identifier, table name and column name
    def select_data(self, host, db_name, table_name, column):

        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT old_data_type, old_data_length, default_constraint, auto_inc_constraint, not_null_constraint, check_constraint, foreign_key_constraint, unique_constraint FROM encrypted_column_data WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND column_name = '{column}'")
            result = DB_Connection.cbdb_cursor.fetchone()

            return result
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Adds the encrypted column data - old data type and
    # foreign key detail if not already in the table
    def add_data(self, host, db_name, table_name, column, old_type, old_length, constraints):

        try:
            has_data = self.select_data(host, db_name, table_name, column)

            if not has_data:
                sql = "INSERT INTO encrypted_column_data (host_identifier, table_name, column_name, old_data_type, old_data_length, default_constraint, auto_inc_constraint, not_null_constraint, check_constraint, foreign_key_constraint, unique_constraint) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                check = str(constraints[3]) if constraints[3] else constraints[3]
                foreign_key = str(constraints[4]) if constraints[4] else constraints[4]
                val = (f"{host}#{db_name}", table_name, column, old_type, old_length, constraints[0], constraints[1], constraints[2], check, foreign_key, constraints[5])

                DB_Connection.cbdb_cursor.execute(sql, val)
                DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes the record of the given host identifier,
    # table name and column name
    def delete_data(self, host, db_name, table_name, column):

        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM encrypted_column_data WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND column_name = '{column}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

class Access_Control_Data(DB_Connection):

    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()

        self.error_msg = error_msg

    ## Selects the access control rules of a given
    # table
    def select_rules(self, host, db_name, table_name):
        
        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT AC.user_id, U.username, AC.key_id FROM access_controls AC LEFT JOIN users U ON U.id = AC.user_id WHERE AC.host_identifier = '{host}#{db_name}' AND AC.table_name = '{table_name}'")
            results = DB_Connection.cbdb_cursor.fetchall()

            return results
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Checks if a rule on the given database, table, user and key
    # already exsits
    def has_rule(self, host, db_name, table_name, user_id, key_id):
        
        try:
            DB_Connection.cbdb_cursor.execute(f"SELECT * FROM access_controls WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND user_id = {user_id} AND key_id = {key_id}")
            results = DB_Connection.cbdb_cursor.fetchall()

            return True if results else False
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return None

    ## Adds an access control rule of the give configs
    #
    def add_rule(self, host, db_name, table_name, user_id, key_id):
        
        try:
            if self.has_rule(host, db_name, table_name, user_id, key_id):
                self.error_msg.set("Access control rule already exists")
                return False
            
            DB_Connection.cbdb_cursor.execute(f"INSERT INTO access_controls (host_identifier, table_name, user_id, key_id) VALUES ('{host}#{db_name}', '{table_name}', {user_id}, {key_id})")
            DB_Connection.cbdb_conn.commit()
            
            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes the given access control rule
    #
    def delete_rule(self, host, db_name, table_name, user_id, key_id):
        
        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM access_controls WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND user_id = {user_id} AND key_id = {key_id}")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes all access control rules of a given key
    # Will be used in encryption removal to delete rules in bulk
    def delete_key_rules(self, host, db_name, table_name, key_id):
        
        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM access_controls WHERE host_identifier = '{host}#{db_name}' AND table_name = '{table_name}' AND key_id = {key_id}")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False

    ## Deletes all access control rules of a given database
    # Will be used in database removal
    def delete_db_rules(self, host, db_name):
        
        try:
            DB_Connection.cbdb_cursor.execute(f"DELETE FROM access_controls WHERE host_identifier = '{host}#{db_name}'")
            DB_Connection.cbdb_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly. Please try again later")
            return False
