from tkinter import StringVar

import unittest

from app.db.database import Users

import app.operation.connect_db as connect_db
import app.db.db_connection as db_connection

## Custom StringVar Class
#
class My_StringVar:

    def __init__(self, initial_value=None):
        self._value = initial_value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

class DB_Connection_Test(unittest.TestCase):

    # Wrong host
    def test_wrong_host(self):
        conn, my_cursor = db_connection.connect("165.154.1.3", "test", "root", "1NandoConor2512!")
        self.assertIsNone(conn) and self.assertIsNone(my_cursor)

    # Wrong password
    def test_wrong_password(self):
        conn, my_cursor = db_connection.connect("127.0.0.1", "test", "root", "wrong")
        self.assertIsNone(conn) and self.assertIsNone(my_cursor)

    # Valid configurations
    def test_valid(self):
        conn, my_cursor = db_connection.connect("127.0.0.1", "test", "root", "1NandoConor2512!")
        self.assertIsNotNone(conn) and self.assertIsNotNone(my_cursor)

class Conn_DB_2_Test(unittest.TestCase):

    # Wrong host
    def test_wrong_host(self):
        error_msg = My_StringVar()
        connect_db.second_step("192.168.50.1", "root", "1NandoConor2512!", error_msg)
        self.assertEqual(error_msg.get, "Operation has failed unexpectedly. Please try again later") and self.assertIsNone(connect_db.database_users)

    # Wrong password
    def test_wrong_password(self):
        error_msg = My_StringVar()
        connect_db.second_step("127.0.0.1", "root", "wrong", error_msg)
        self.assertEqual(error_msg.get, "Operation has failed unexpectedly. Please try again later") and self.assertIsNone(connect_db.database_users)

    # Valid configurations
    def test_valid_configs(self):
        error_msg = My_StringVar()
        connect_db.second_step("127.0.0.1", "root", "1NandoConor2512!", error_msg)
        self.assertIsNotNone(connect_db.database_users)

class Match_Role_Test(unittest.TestCase):
    
    # Valid configurations
    def test_valid_configs(self):
        all_users = [('cbdb_user', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'), ('debian-sys-maint', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y'), ('mysql.infoschema', 'Y', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'), ('mysql.session', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'Y', 'N', 'N', 'N', 'N'), ('mysql.sys', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N'), ('root', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y', 'Y')]
        users = connect_db.match_role(all_users)
        self.assertEqual(users, {'debian-sys-maint': 'admin', 'mysql.infoschema': 'user', 'root': 'admin'})

class Remove_User_Test(unittest.TestCase):

    # Invalid Username
    def test_invalid_username(self):
        error_msg = My_StringVar()
        connect_db.database_users = {'root': 'admin'}
        connect_db.remove_user("invalid", error_msg)
        self.assertEqual(error_msg.get(), "Remove operation has failed unexpectedly. Please try again later")

    # Valid Username
    def test_valid_username(self):
        error_msg = My_StringVar()
        connect_db.database_users = {'root': 'admin'}
        connect_db.remove_user("root", error_msg)
        self.assertEqual(connect_db.database_users, {})

class Add_Users_Test(unittest.TestCase):

    # Valid configurations
    def test_valid_configs(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        users_added = CONN_DBS.add_users("localhost", "test", {'test-user': 'admin'})
        self.assertEqual(users_added)


if __name__ == "__main__":
    unittest.main()
