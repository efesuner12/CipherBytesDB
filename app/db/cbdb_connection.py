import app.db.db_connection as db_connection
import app.db.db_configs as db_configs

# The concept of this class is "an always active class"
# where the class variables are set at application startup
# and used when needed
class DB_Connection:

    CBDB_CONFIG_FILE = "~/.config/cipherbytesdb/db_configs.conf"
    EKMS_CONFIG_FILE = "~/.config/cipherbytesdb/ekms_db_configs.conf"

    USER_PASSWORD = ""

    ## Establishes a connection to the
    # cipherbytesdb database and to the EKMS
    # by reading the configurations from the config files
    @classmethod
    def establish_connections(cls):
        cbdb_configs = db_configs.read_configs(cls.CBDB_CONFIG_FILE, cls.USER_PASSWORD)
        cls.cbdb_conn, cls.cbdb_cursor = db_connection.connect(cbdb_configs)

        ekms_configs = db_configs.read_configs(cls.EKMS_CONFIG_FILE, cls.USER_PASSWORD)
        cls.ekms_conn, cls.ekms_cursor = db_connection.connect(ekms_configs)

    ## Closes the open MySQL connections
    # to the cipherbytesdb database and to the EKMS
    # if the connection variables are created
    @classmethod
    def close_connections(cls):

        if hasattr(cls, 'cbdb_conn') and cls.cbdb_conn and cls.cbdb_conn.is_connected():
            cls.cbdb_conn.close()

        if hasattr(cls, 'ekms_conn') and cls.ekms_conn and cls.ekms_conn.is_connected():
            cls.ekms_conn.close()

    def __init__(self):
        pass
