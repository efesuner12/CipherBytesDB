from app.db.database import Table_Encryption_Model

import app.db.db_connection as db_connection
import app.operation.db_password as db_password

db_tables = {}

## Returns a list of all tables of a database
#
def get_db_tables(host, db_name, db_nick, username, error_msg):
    password = db_password.get_password(host, db_name, db_nick, error_msg)

    conn = None

    try:
        conn, my_cursor = db_connection.connect({"host": host, "database": db_name, "user": username, "password": password})

        my_cursor.execute(f"SHOW TABLES")
        all_tables = my_cursor.fetchall()

        tables = [table[0] for table in all_tables]

        return tables
    except Exception:
        error_msg.set("Operation has failed unexpectedly. Please try again later")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()

## Generates the database view
# + Gets all tables of the database
# + Gets all encrypted tables of the database
# + Sets the global dictionary of each table and their details:
# ++ Encrypted
# ++ Encryption Models
def gen_db_view(host, db_name, db_nick, username, error_msg):
    db_tables.clear()

    all_tables = get_db_tables(host, db_name, db_nick, username, error_msg)

    if len(all_tables) > 0:
        TABLE_ENC_MODEL = Table_Encryption_Model(error_msg)
        all_enc_tables = TABLE_ENC_MODEL.select_table_encryption(host, db_name)

        enc_tables = {}

        for enc_table in all_enc_tables:
            table_name = enc_table[0]

            if not table_name in enc_tables:
                enc_tables[table_name] = [enc_table[1]]
            else:
                enc_tables[table_name].append(enc_table[1])

        # "<table>":[<is_encrypted>, [<enc_models>]]
        for table in all_tables:
            is_encrypted = 'Y' if table in enc_tables else 'N'

            enc_model = enc_tables.get(table) if is_encrypted == 'Y' else []

            for i in range(len(enc_model)):
                if enc_model[i] == '0':
                    enc_model[i] = "Table Level Encryption"
                elif enc_model[i] == '1':
                    enc_model[i] = "Column Level Encryption"
                elif enc_model[i] == '2':
                    enc_model[i] = "Row Level Encryption"
                elif enc_model[i] == '3':
                    enc_model[i] = "Cell Level Encryption"

            db_tables[table] = [is_encrypted, enc_model]
