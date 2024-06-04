import unittest

from app.operation.validation import Validater
from app.db.database import Admin_Database

import app.operation.cryptography.hash as hasher
import app.operation.login as login

## Custom StringVar Class
#
class My_StringVar:

    def __init__(self, initial_value=None):
        self._value = initial_value

    def set(self, value):
        self._value = value

    def get(self):
        return self._value

# Dummy function in replacement of show_home_page
def dummy_1():
    0

# Dummy function in replacement of show_conn_db_page
def dummy_2():
    0

## Tests the username validation function
#
class Validater_Test(unittest.TestCase):
    
    # Uppercase
    def test_uppercase_username(self):
        VALIDATER = Validater()

        is_valid_1 = VALIDATER.valid_username("ADMIN")
        self.assertFalse(is_valid_1)
    
    # Space
    def test_username_space(self):
        VALIDATER = Validater()

        is_valid_2 = VALIDATER.valid_username("ad min")
        self.assertFalse(is_valid_2)

    # Valid
    def test_valid_username(self):
        VALIDATER = Validater()

        is_valid_3 = VALIDATER.valid_username("admin")
        self.assertTrue(is_valid_3)

## Tests the whole hashing operation by
# first hashing a string then validating it
class Hash_Test(unittest.TestCase):     

    # Wrong password
    def test_wrong_str(self):
        hash_1 = hasher.hash("password")

        is_valid_password_1 = hasher.validate("wrong", hash_1)
        self.assertFalse(is_valid_password_1)

    # Correct password
    def test_correct_str(self):
        hash_1 = hasher.hash("password")
        
        is_valid_password_2 = hasher.validate("password", hash_1)        
        self.assertTrue(is_valid_password_2)

## Tests login database operations
#
class Login_DB_Test(unittest.TestCase):

    # Invalid username
    def test_invalid_uname_has_uname(self):
        error_msg = My_StringVar()
        ADMIN_DB = Admin_Database(error_msg)

        has_uname_1 = ADMIN_DB.has_username("User")
        self.assertEqual(error_msg.get(), "Please enter a valid username")

    # Non-existing username
    def test_has_no_username(self):
        error_msg = My_StringVar()
        ADMIN_DB = Admin_Database(error_msg)

        has_uname_2 = ADMIN_DB.has_username("user")
        self.assertFalse(has_uname_2)

    # Existing username
    def test_has_username(self):
        error_msg = My_StringVar()
        ADMIN_DB = Admin_Database(error_msg)

        has_uname_3 = ADMIN_DB.has_username("admin")
        self.assertIsNone(has_uname_3)

    # Invalid username
    def test_invalid_uname_select_password(self):
        error_msg = My_StringVar()
        ADMIN_DB = Admin_Database(error_msg)

        password = ADMIN_DB.select_password("User")
        self.assertEqual(error_msg.get(), "Please enter a valid username")

    # Valid operation
    def test_select_password(self):
        error_msg = My_StringVar()
        ADMIN_DB = Admin_Database(error_msg)

        password = ADMIN_DB.select_password("admin")
        self.assertIsNotNone(password)

## Tests the login function
#
class Login_Test(unittest.TestCase):

    # Empty password
    def test_login(self):
        error_msg = My_StringVar()

        username_input = My_StringVar()
        username_input.set("admin")

        password_input = My_StringVar()
        password_input.set("")

        login.login(username_input, password_input, error_msg, dummy_1, dummy_2)
        self.assertEqual(error_msg.get(), "Both username and password fields are required")

    # Invalid username - check if set in db level
    def test_invalid_uname(self):
        error_msg = My_StringVar()

        username_input = My_StringVar()
        username_input.set("USER")

        password_input = My_StringVar()
        password_input.set("password")

        login.login(username_input, password_input, error_msg, dummy_1, dummy_2)
        self.assertEqual(error_msg.get(), "Please enter a valid username")

    # Non-existing username
    def test_non_existing_uname(self):
        error_msg = My_StringVar()

        username_input = My_StringVar()
        username_input.set("user")

        password_input = My_StringVar()
        password_input.set("password")

        login.login(username_input, password_input, error_msg, dummy_1, dummy_2)
        self.assertEqual(error_msg.get(), "Incorrect password")

    # Wrong password
    def test_wrong_password(self):
        error_msg = My_StringVar()

        username_input = My_StringVar()
        username_input.set("admin")

        password_input = My_StringVar()
        password_input.set("te")

        login.login(username_input, password_input, error_msg, dummy_1, dummy_2)
        self.assertEqual(error_msg.get(), "Incorrect password")

    # Correct credentials
    def test_correct_creds(self):
        error_msg = My_StringVar()

        username_input = My_StringVar()
        username_input.set("admin")

        password_input = My_StringVar()
        password_input.set("test")

        logged_in = login.login(username_input, password_input, error_msg, dummy_1, dummy_2)
        self.assertTrue(logged_in)
