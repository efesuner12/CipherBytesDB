from app.db.database import Connected_Databases, Users, Table_Encryption_Model, Access_Control_Data
from app.operation.ekms_api import EKMS_API

import app.db.db_connection as db_connection
import app.operation.db_password as db_password
import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor
import app.operation.cryptography.ecc as ecc

connected_dbs = {}

## Returns a dictionary of connected databases 
# by fetching them using the database function
# and generating the dictionary
def get_connections(error_msg):
    connected_dbs.clear()

    CONNECTED_DBS = Connected_Databases(error_msg)
    dbs = CONNECTED_DBS.select_connected_databases()

    if not dbs:
        return

    # index 0 : host -> key sub 1
    # index 1 : database name -> key sub 2
    # index 2 : username -> value - list index 0
    # index 3 : database nickname -> value - list index 1
    # index 4 : key rotation interval - list index 2
    # "<host>:<db_name>":[<username>, <db_nick>, <key_rotation_interval>]
    for db in dbs:
        host = db[0]
        db_name = db[1]
        username = db[2]
        db_nick = db[3]
        key_rotation_interval = db[len(db)-1]
        
        key_val = f"{host}:{db_name}"
        list_val = [username, db_nick, key_rotation_interval]

        connected_dbs[key_val] = list_val

## Gets the stored password and compares
# it with the password input
def check_password(host, db_name, db_nick, password_input, error_msg):
    input_password = password_input.get()

    if input_password == "":
        error_msg.set("Current password field is required")
        return False

    password = db_password.get_password(host, db_name, db_nick, error_msg)

    if password:
        correct_password = password == input_password

        if not correct_password:
            error_msg.set("Incorrect password")
            return False

        return True
    
    return False

## Performs the password update operation
# + Get new passwords inputs
# + Check if either is blank
# + Check if they are equal
# + Test connection with the new password
# + Delete the current keys from the ekms and the host
# + Encrypt the new password (adds the new key to ekms)
# + Update the password in database
def update_password(host, db_name, db_nick, username, new_password, new_password_repeat, key_rotation_interval, error_msg):
    input_new_password = new_password.get()
    input_new_password_repeat = new_password_repeat.get()

    if input_new_password == "" or input_new_password_repeat == "":
        error_msg.set("Both new password and\nrepeat new password fields are required")
        return False

    if input_new_password != input_new_password_repeat:
        error_msg.set("Password inputs do not match")
        return False

    can_connect = db_connection.test_connection(host, db_name, username, input_new_password)

    if not can_connect:
        error_msg.set(f"Cannot connect to {host}:{db_name}.\nPlease check your configs and try again")
        return False

    metadata = f"{host}#{db_name}#{db_nick}"
    hashed_metadata = hasher.sha_512_hash(metadata)

    ekms = EKMS_API(error_msg)
    enc_keys_removed = ekms.delete_key_pair(hashed_metadata)

    user_keys_removed = ecc.delete_key_pair(hashed_metadata, error_msg) if enc_keys_removed else False
    
    if user_keys_removed:
        nonce = aes_encryptor.generate_nonce()
        key = aes_encryptor.generate_key(hashed_metadata, key_rotation_interval, error_msg)
        new_password_enc = aes_encryptor.encrypt(input_new_password, hashed_metadata, key, nonce, error_msg)

        if new_password_enc:
            CONNECTED_DBS = Connected_Databases(error_msg)
            return CONNECTED_DBS.update_password(host, db_name, new_password_enc)

## Perfoms the edit connection operation of a database connection
# + Get old stored values
# + Get new values
# + Identify the changed ones and set the same ones to None
# + If username is changed
# ++ Test connection with the new username
# + If database nickname is changed
# ++ Update the password ciphertext with the new metadata
# ++ Update the metadata in ekms
# ++ Update the file names of user's ECC key pair
# + If key rotation interval is changed
# ++ Update the expiration time in ekms
# + If none are changed raise an error
# + Call the database operation if there are changed values
def edit_connection(host, db_name, new_db_nick, new_username, new_key_rotation, error_msg):
    
    # Get the old configs according to the key choice of the dic
    for key, value in connected_dbs.items():
        old_username = value[0]
        old_db_nick = value[1]
        old_key_interval = value[2]

        stored_host = key.split(":")[0]
        stored_db_name = key.split(":")[1]
        
        if stored_host == host and stored_db_name == db_name:
            break

    new_db_nick_input = new_db_nick.get()
    new_username_input = new_username.get()
    new_key_rotation_interval = new_key_rotation.get()

    new_db_nick_input = None if new_db_nick_input == old_db_nick or new_db_nick_input == "Database Nickname" else new_db_nick_input
    new_username_input = None if new_username_input == old_username else new_username_input
    new_key_rotation_interval = None if new_key_rotation_interval == old_key_interval else new_key_rotation_interval

    CONNECTED_DBS = Connected_Databases(error_msg)

    # if username is changed test connection with the new username
    if new_username_input:
        password = db_password.get_password(host, db_name, old_db_nick, error_msg)

        if not password:
            return False

        can_connect = db_connection.test_connection(host, db_name, new_username_input, password)

        if not can_connect:
            error_msg.set(f"Cannot connect to {host}:{db_name} using {new_username_input}.\nPlease check the username and try again")
            return False

    old_metadata = f"{host}#{db_name}#{old_db_nick}"
    old_hashed_metadata = hasher.sha_512_hash(old_metadata)

    new_hashed_metadata = ""

    ekms = EKMS_API(error_msg)

    # if database nickname is updated then update the metadata in EKMS 
    # and the password ciphertext in the database
    if new_db_nick_input:
        new_metada = f"{host}#{db_name}#{new_db_nick_input}"
        new_hashed_metadata = hasher.sha_512_hash(new_metada)

        # re encrypt with the same key and nonce
        password = db_password.get_password(host, db_name, old_db_nick, error_msg)

        enc_key, user_priv_key, user_pub_key = aes_encryptor.generate_encryption_key(old_hashed_metadata, error_msg)

        enc_password = CONNECTED_DBS.select_password(host, db_name)[0]
        enc_password = bytes.fromhex(enc_password)
        aad = enc_password[0:76]
        nonce = aad[0:12]

        new_password_enc = aes_encryptor.encrypt(password, new_hashed_metadata, enc_key, nonce, error_msg)

        password_updated = CONNECTED_DBS.update_password(host, db_name, new_password_enc) if new_password_enc else False

        metadata_updated = ekms.update_metadata(old_hashed_metadata, new_hashed_metadata) if password_updated else False

        files_deleted = ecc.delete_key_pair(old_hashed_metadata, error_msg) if metadata_updated else False
        
        files_updated = ecc.write_key_pair(new_hashed_metadata, user_priv_key, user_pub_key, error_msg) if files_deleted and user_priv_key and user_pub_key else False

        if not files_updated:
            return False

    # if key rotation interval is updated then update the expire time in EKMS
    if new_key_rotation_interval:
        metadata = new_hashed_metadata if new_db_nick_input else old_hashed_metadata
        expire_time_updated = ekms.update_key_expire_time(metadata, new_key_rotation_interval)

        if not expire_time_updated:
            return False

    # Calls the database operation only if a config is changed
    if all(config == None for config in [new_db_nick_input, new_username_input, new_key_rotation_interval]):
        error_msg.set("No changes have been made")
        return False

    return CONNECTED_DBS.update_database_connection(host, db_name, new_db_nick_input, new_username_input, new_key_rotation_interval)

## Disconnects database: 
# + Checks if there are active encryptions on the database
# + Removes from connected_dbs
# + Removes the users
# + Deletes its password's key in EKMS and the host
# + Deletes its access control rules
def disconnect_database(host, db_name, db_nick, error_msg):

    TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
    all_enc_tables = TABLE_ENC_MODEL.select_table_encryption(host, db_name)

    if len(all_enc_tables) > 0:
        error_msg.set("Please remove active encryptions to disconnect\nthe database")
        return False

    CONNECTED_DBS = Connected_Databases(error_msg)
    db_disconnected = CONNECTED_DBS.delete_database(host, db_name)

    # Database errors raised in db level
    if db_disconnected:
        USERS = Users(error_msg)
        users_deleted = USERS.delete_users(host, db_name)

        if users_deleted:
            metadata = f"{host}#{db_name}#{db_nick}"
            hashed_metadata = hasher.sha_512_hash(metadata)

            ekms = EKMS_API(error_msg)
            enc_keys_deleted = ekms.delete_key_pair(hashed_metadata)

            user_keys_deleted = ecc.delete_key_pair(hashed_metadata, error_msg) if enc_keys_deleted else False

            if user_keys_deleted:
                access_control_db = Access_Control_Data(error_msg)
                
                return access_control_db.delete_db_rules(host, db_name)

    return False
