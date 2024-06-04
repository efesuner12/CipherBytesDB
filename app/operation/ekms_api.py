import datetime

from app.db.cbdb_connection import DB_Connection

class EKMS_API(DB_Connection):

    def __init__(self, error_msg):
        # Inherits from DB_Connection - uses its variables and functions
        super().__init__()

        self.error_msg = error_msg

    ## Generates the expiration datetime based on the current
    # datetime and the key rotation interval
    def get_expiration_datetime(self, current, key_rotation_interval):

        if not current or not key_rotation_interval:
            return None

        if key_rotation_interval == "Yearly":
            expire_time = current + datetime.timedelta(days=365)
        elif key_rotation_interval == "Monthly":
            expire_time = current + datetime.timedelta(days=30)
        elif key_rotation_interval == "Weekly":
            expire_time = current + datetime.timedelta(days=7)
        elif key_rotation_interval == "Daily":
            expire_time = current + datetime.timedelta(days=1)

        return expire_time.strftime("%Y-%m-%d %H:%M:%S")

    ## Posts the key pair to the EKMS and gets the expiration time
    # based on the key rotation interval
    # If expiration time is None, the operation will fail
    def post_key_pair(self, priv_key, pub_key, metadata, key_rotation_interval):

        try:
            current = datetime.datetime.now()
            expire_time = self.get_expiration_datetime(current, key_rotation_interval)

            insert_command = "INSERT INTO encryption_keys (encryption_priv_key, encryption_pub_key, expiration_datetime, encryption_metadata) VALUES (%s, %s, %s, %s)"
            val = (priv_key, pub_key, expire_time, metadata)

            DB_Connection.ekms_cursor.execute(insert_command, val)
            DB_Connection.ekms_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Returns the encryption private key of the given metadata
    #
    def get_priv_key(self, metadata):
        
        try:
            DB_Connection.ekms_cursor.execute(f"SELECT encryption_priv_key FROM encryption_keys WHERE encryption_metadata = '{metadata}'")
            results = DB_Connection.ekms_cursor.fetchone()

            return results
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Returns the encryption public key of the given metadata
    #
    def get_pub_key(self, metadata):
        
        try:
            DB_Connection.ekms_cursor.execute(f"SELECT encryption_pub_key FROM encryption_keys WHERE encryption_metadata = '{metadata}'")
            results = DB_Connection.ekms_cursor.fetchone()

            return results
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Deletes the key with the given metadata
    #
    def delete_key_pair(self, metadata):

        try:
            DB_Connection.ekms_cursor.execute(f"DELETE FROM encryption_keys WHERE encryption_metadata = '{metadata}'")
            DB_Connection.ekms_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Updates the metadata of the key
    #
    def update_metadata(self, old_metadata, new_metada):

        try:
            DB_Connection.ekms_cursor.execute(f"UPDATE encryption_keys SET encryption_metadata = '{new_metada}' WHERE encryption_metadata = '{old_metadata}'")
            DB_Connection.ekms_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Updates the expiration time with the new key rotation interval
    # If new expiration time is None, the operation will fail
    def update_key_expire_time(self, metadata, new_key_rotation):

        try:
            DB_Connection.ekms_cursor.execute(f"SELECT creation_datetime FROM encryption_keys WHERE encryption_metadata = '{metadata}'")
            current = DB_Connection.ekms_cursor.fetchall()

            expire_time = self.get_expiration_datetime(current[0][0], new_key_rotation)

            DB_Connection.ekms_cursor.execute(f"UPDATE encryption_keys SET expiration_datetime = '{expire_time}' WHERE encryption_metadata = '{metadata}'")
            DB_Connection.ekms_conn.commit()

            return True
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return False

    ## Checks if the key with the given metadata
    # exists
    def check_key_existance(self, metadata):

        try:
            DB_Connection.ekms_cursor.execute(f"SELECT COUNT(encryption_priv_key) FROM encryption_keys WHERE encryption_metadata = '{metadata}'")
            count = DB_Connection.ekms_cursor.fetchone()

            return count[0] > 0
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Gets the key ID of the given metadata
    #
    def get_key_id(self, metadata):

        try:
            DB_Connection.ekms_cursor.execute(f"SELECT id FROM encryption_keys WHERE encryption_metadata = '{metadata}'")
            key_id = DB_Connection.ekms_cursor.fetchone()

            return key_id[0]
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None

    ## Checks if a key exists with the given ID
    #
    def has_key(self, key_id):
        
        try:
            DB_Connection.ekms_cursor.execute(f"SELECT COUNT(id) FROM encryption_keys WHERE id = {key_id}")
            result = DB_Connection.ekms_cursor.fetchone()

            return int(result[0]) > 0
        except Exception:
            self.error_msg.set("Operation has failed unexpectedly.\nPlease try again later")
            return None
