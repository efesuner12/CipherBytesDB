from tkinter import StringVar

import mysql.connector

from app.db.database import Connected_Databases, Users
from app.operation.validation import Validater

import app.db.db_connection as db_connection
import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor

database_host = ""
database_name = ""
database_users = {}

## Performs the connect new database operation's first step
# + Get host, database name, database nickname, username and password
# to connect to the database
# + Check if host or database name or username or password are blank
# + Check if the host and db name pair already exists - validates the host
# + Validate username input
# + Test connection
# ++ Generate and hash the metadata of the encryption
# ++ Encrypt the password
# ++ Add configurations to the database
# ++ Set the input variables to blank
# ++ Set the global variable db name to current db name
# ++ Run second step
# ++ Redirect to second step
def first_step(host, db_name, db_nick, username, password, key_rotation_interval, error_msg, show_conn_db_2_page):
    input_host = host.get()
    input_db_name = db_name.get()
    input_db_nick = db_nick.get()
    input_username = username.get()
    input_password = password.get()
    input_key_rotation_interval = key_rotation_interval.get()

    if input_host == "" or input_db_name == "" or input_username == "" or input_password == "":
        error_msg.set("Host, database name, username and password fields are required")
        return

    CONNECTED_DBS = Connected_Databases(error_msg)

    has_the_connection = CONNECTED_DBS.has_connection(input_host, input_db_name)
    
    if has_the_connection == None:
        return
    elif has_the_connection:
        error_msg.set(f"{input_host}:{input_db_name} already exists")
        return

    VALIDATER = Validater()

    if not VALIDATER.valid_username(input_username):
        error_msg.set("Please enter a valid username")
        return

    can_connect = db_connection.test_connection(input_host, input_db_name, input_username, input_password)

    if not can_connect:
        error_msg.set(f"Cannot connect to {input_host}:{input_db_name}.\nPlease check your configs and try again")
        return

    error_msg.set("")

    # localhost and 127.0.0.1 are the same
    input_host = "localhost" if input_host == "127.0.0.1" else input_host

    metadata = f"{input_host}#{input_db_name}#{input_db_nick}"
    hashed_metadata = hasher.sha_512_hash(metadata)
    nonce = aes_encryptor.generate_nonce()
    key = aes_encryptor.generate_key(hashed_metadata, input_key_rotation_interval, error_msg)
    enc_password = aes_encryptor.encrypt(input_password, hashed_metadata, key, nonce, error_msg)

    if enc_password:
        new_conn_added = CONNECTED_DBS.add_new_connection(input_host, input_db_name, input_db_nick, input_username, enc_password, input_key_rotation_interval)

        if new_conn_added:
            host.set("")
            db_name.set("")
            db_nick.set("")
            username.set("")
            password.set("")
            key_rotation_interval.set("")

            global database_host
            database_host = input_host

            global database_name
            database_name = input_db_name

            # Second step's error msg
            second_step_error_msg = StringVar()
            
            second_step(input_host, input_username, input_password, second_step_error_msg)

            show_conn_db_2_page(second_step_error_msg)

## For each user examine the privilages
# and return a dic of users and their role
def match_role(users):
    final_users = {}

    for user in users:
        username = user[0]
        role = ""
        
        # Lazy Evaluation
        # + Disregard if all are N or below are not satisfied
        # + if select, insert, update, delete, create and drop are Y then admin
        # + if file, super, execute, create user, create role and drop role are Y then admin
        # + if any of the select and insert or both are Y then user
        if all(priv == 'Y' for priv in user[3:7]) or all(priv == 'Y' for priv in user[7:13]):
            role = "admin"
        elif any(priv == 'Y' for priv in user[1:3]):
            role = "user"
        
        if role:
            final_users[username] = role

    return final_users

## Performs the connect new database operation's second step
# + Fetch the users and their privileges from the connected database
# + Match roles based on their privileges
def second_step(host, username, password, error_msg):
    conn = None
    
    try:
        conn, my_cursor = db_connection.connect({"host": host, "database": "mysql", "user": username, "password": password})

        host = "localhost" if host == "127.0.0.1" else host

        my_cursor.execute(f"""
        SELECT User, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv, 
        File_priv, Super_priv, Execute_priv, Create_user_priv, Create_role_priv, Drop_role_priv
        FROM mysql.user 
        WHERE Host = '{host}'
        """)
        
        all_users = my_cursor.fetchall()

        users = match_role(all_users)
        
        global database_users
        database_users = users
    except mysql.connector.Error:
        error_msg.set("Operation has failed unexpectedly. Please try again later")
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()

## Removes the given user from the dic
#
def remove_user(username, error_msg):
    try:
        removed_user = database_users.pop(username)
    except KeyError:
        error_msg.set("Remove operation has failed unexpectedly. Please try again later")
        return None

## Adds the users to the database by
# calling the database function
def add_users(error_msg):
    USERS = Users(error_msg)
    return USERS.add_users(database_host, database_name, database_users)
