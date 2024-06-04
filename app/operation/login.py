from app.db.database import DB_Connection, Admin_Database, Connected_Databases

import app.operation.cryptography.hash as hasher
import app.operation.master_sk as master_sk

logged_in = False

## Performs the login operations:
# + Get username and password inputs
# + Check if they are empty and raise an error
# + Set DB connection user password and
# call the initiation function
# + Call master symmetric key creation
# + Check if the username exists - username validated
# + Check if the password input matches the stored password
# + Check if there are connected databases to the application
# and switch pages accordingly
# + Set the input variables to blank
def login(username, password, error_msg, show_home_page, show_conn_db_page):
    input_username = username.get()
    input_password = password.get()

    if input_username == "" or input_password == "":
        error_msg.set("Both username and password fields are required")
        return

    DB_Connection.USER_PASSWORD = input_password
    DB_Connection.establish_connections()

    master_sk.create_master_sk(error_msg)

    ADMIN_DB = Admin_Database(error_msg)

    # if username is present in the db, the programme will carry on
    # if the db function returns false, an error will be raised here
    # if the db functions return None, the error msg set on db level will be printed
    # if username is not valid, the error msg set on db level will be printed
    has_username = ADMIN_DB.has_username(input_username)

    if has_username:
        db_passwords = ADMIN_DB.select_password(input_username)
        
        if len(db_passwords) > 0 and hasher.validate(input_password, db_passwords[0]):
            error_msg.set("")

            global logged_in
            logged_in = True

            CONNECTED_DBS = Connected_Databases(error_msg)

            if CONNECTED_DBS.has_connected_dbs():
                show_home_page()
            else:
                show_conn_db_page()

            username.set("")
            password.set("")

            return True
        else:
            error_msg.set("Incorrect password")
            return
    elif has_username == False:
        error_msg.set("Username doesn't exist")
        return
