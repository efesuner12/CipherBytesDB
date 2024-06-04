import mysql.connector

import app.db.db_connection as db_connection

## Returns all of the columns of a table in the same order
# they are in the table view
def get_all_columns(host, db_name, username, password, table_name, error_msg):
    conn = None

    try:
        conn, my_cursor = db_connection.connect({"host": host, "database": db_name, "user": username, "password": password})

        my_cursor.execute(f"SELECT column_name FROM information_schema.COLUMNS WHERE table_schema = '{db_name}' AND table_name = '{table_name}' ORDER BY ordinal_position")
        columns = my_cursor.fetchall()

        return columns
    except Exception:
        error_msg.set("Fetching the columns has failed unexpectedly. Please try again later")
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()
