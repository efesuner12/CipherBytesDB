from tkinter import StringVar

import unittest

from app.operation.validation import Validater
from app.db.database import Connected_Databases

import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor
import app.db.db_connection as db_connection
import app.operation.connect_db as conn_db

## Custom StringVar Class
#
class My_StringVar:

    def __init__(self, initial_value=None):
        self._value = initial_value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

## Tests the host validation function
#
class Validater_Test(unittest.TestCase):

    # localhost
    def test_localhost(self):
        VALIDATER = Validater()
        is_valid_1 = VALIDATER.valid_host("localhost")
        self.assertTrue(is_valid_1)

    # Invalid IPv4
    def test_invalid_ipv4(self):
        VALIDATER = Validater()
        is_valid_2 = VALIDATER.valid_host("192.168..1")
        self.assertFalse(is_valid_2)

    # Invalid IPv6
    def test_invalid_ipv6(self):
        VALIDATER = Validater()
        is_valid_3 = VALIDATER.valid_host("2001:db8:3333:4444::::00")
        self.assertFalse(is_valid_3)

    # IPv4
    def test_ipv4(self):
        VALIDATER = Validater()
        is_valid_4 = VALIDATER.valid_host("192.168.1.100")
        self.assertTrue(is_valid_4)

    # IPv6
    def test_ipv6(self):
        VALIDATER = Validater()
        is_valid_5 = VALIDATER.valid_host("2001:db8:3333:4444:5555:6666:7777:8888")
        self.assertTrue(is_valid_5)

## Tests SHA-512 hash function
#
class Hash_Test(unittest.TestCase):


    # Wrong
    def test_hash_function_1(self):
        org_hash = "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff"
        hash_1 = hasher.sha_512_hash("wrong")
        self.assertNotEqual(hash_1, org_hash)
    
    # Correct
    def test_hash_function_2(self):
        org_hash = "ee26b0dd4af7e749aa1a8ee3c10ae9923f618980772e473f8819a5d4940e0db27ac185f8a0e1d5f84f88bc887fd67b143732c304cc5fa9ad8e6f57f50028a8ff"
        hash_2 = hasher.sha_512_hash("test")
        self.assertEqual(hash_2, org_hash)

## Tests connect db database operations
#
class Conn_DB_DB_Test(unittest.TestCase):

    # No of connected dbs - needs a connection in db
    def test_has_conn_dbs(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        has = CONN_DBS.has_connected_dbs()
        self.assertTrue(has)

    # Non-existing host
    def test_has_conn_non_existing_host(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        has_conn_1 = CONN_DBS.has_connection("192.168.1.20", "test")
        self.assertFalse(has_conn_1)

    # Invalid host
    def test_has_conn_invalid_host(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        has_conn_2 = CONN_DBS.has_connection("192.168..", "test")
        self.assertEqual(error_msg.get(), "Please enter a valid host address")

    # Non-existing DB Name
    def test_has_conn_non_existing_db(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        has_conn_2 = CONN_DBS.has_connection("localhost", "invalid")
        self.assertFalse(has_conn_2)

    # Valid configurations - needs a connection in db
    def test_has_conn(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        has_conn_3 = CONN_DBS.has_connection("localhost", "test")
        self.assertTrue(has_conn_3)

    # 127.0.0.1 and localhost - needs a connection in db
    def test_has_conn_localhost(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        has_conn_4 = CONN_DBS.has_connection("127.0.0.1", "test")
        self.assertTrue(has_conn_4)

    # Duplicate connection - needs a connection in db
    def test_add_duplicate_conn(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        is_added = CONN_DBS.add_new_connection("localhost", "test", "", "root", "", "Monthly")
        self.assertEqual(error_msg.get(), "##")
    
    # Duplicate connection 2 - needs a connection in db
    def test_add_duplicate_conn_2(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        is_added_2 = CONN_DBS.add_new_connection("127.0.0.1", "test", "", "root", "", "Yearly")
        self.assertEqual(error_msg.get(), "##")

    # Invalid host
    def test_add_invalid_conn(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        is_added_3 = CONN_DBS.add_new_connection("127...0.", "test", "", "root", "", "Weekly")
        self.assertEqual(error_msg.get(), "Please enter a valid host address")

    # Invalid username
    def test_add_invalid_conn_2(self):
        error_msg = My_StringVar()
        CONN_DBS = Connected_Databases(error_msg)

        is_added_4 = CONN_DBS.add_new_connection("127.0.0.1", "TEST", "", "root", "", "Daily")
        self.assertEqual(error_msg.get(), "Please enter a valid username")

## Test test connection function
#
class Test_Conn_Test(unittest.TestCase):
    
    # Invalid host
    def test_invalid_host(self):
        can_conn_1 = db_connection.test_connection("192.168.1.20", "test", "root", "1NandoConor2512!")
        self.assertFalse(can_conn_1)

    # Invalid database name
    def test_invalid_db_name(self):
        can_conn_2 = db_connection.test_connection("localhost", "invalid", "root", "1NandoConor2512!")
        self.assertFalse(can_conn_2)

    # Invalid username
    def test_invalid_uname(self):
        can_conn_3 = db_connection.test_connection("localhost", "test", "user", "1NandoConor2512!")
        self.assertFalse(can_conn_3)

    # Invalid password
    def test_invalid_password(self):
        can_conn_4 = db_connection.test_connection("localhost", "test", "root", "pass")
        self.assertFalse(can_conn_4)

    # All valid
    def test_valid_configs(self):
        can_conn_5 = db_connection.test_connection("localhost", "test", "root", "1NandoConor2512!")
        self.assertTrue(can_conn_5)

## Tests the connect db function
#
class Conn_DB_Test(unittest.TestCase):

    # Blank configs
    def test_blank_configs(self):
        error_msg = My_StringVar()

        conn_db.first_step("", "", "nick", "root", "1NandoConor2512!", "", error_msg, "")
        self.assertEqual(error_msg, "Host, database name, username and password fields are required")

    # Invalid host - check if set in db level
    def test_invalid_host(self):
        error_msg = My_StringVar()

        conn_db.first_step("192...168", "test", "", "root", "1NandoConor2512!", "Weekly",error_msg, "")
        self.assertEqual(error_msg, "Please enter a valid host address")

    # Invalid username
    def test_invalid_username(self):
        error_msg = My_StringVar()

        conn_db.first_step("localhost", "test", "", "UserNAME", "1NandoConor2512!", "Daily", error_msg, "")
        self.assertEqual(error_msg, "Please enter a valid username")

    # Duplicate connection - needs a connection in db
    def test_duplicate_connection(self):
        error_msg = My_StringVar()

        conn_db.first_step("localhost", "test", "", "root", "1NandoConor2512!", "Monthly", error_msg, "")
        self.assertEqual(error_msg, "localhost:test already exists!")

    # Connection error
    def test_connection_error(self):
        error_msg = My_StringVar()

        conn_db.first_step("localhost", "test", "", "root", "password", "Monthly", error_msg, "")
        self.assertEqual(error_msg, "Cannot connect to localhost:test.\nPlease check your configs and try again")

    # Valid configs - check global variable database_name
    def test_conn_db(self):
        error_msg = My_StringVar()

        conn_db.first_step("localhost", "VisionDB", "", "root", "1NandoConor2512!", "Monthly", error_msg, "")
        self.assertEqual(conn_db.database_name, "VisionDB")


if __name__ == "__main__":
    unittest.main()
