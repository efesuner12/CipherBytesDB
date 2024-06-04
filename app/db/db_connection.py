import mysql.connector

## Tests the connection to the MySQL database
# with the given configurations
def test_connection(host, db_name, username, password):
    conn = None

    try:
        conn = mysql.connector.connect(host=host, database=db_name, user=username, password=password)
        my_cursor = conn.cursor()

        return True
    except mysql.connector.Error:
        return False
    finally:
        if conn and conn.is_connected():
            conn.close()

## Connects to the MySQL database using
# the given settings
# Returns the connection and the cursor
# if successfully connected else None
def connect(configs):
    try:
        conn = mysql.connector.connect(**configs)
        my_cursor = conn.cursor()

        return conn, my_cursor
    except Exception:
        return None, None
