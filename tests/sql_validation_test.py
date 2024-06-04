import unittest

from app.api.requests.handle_requests import Request_Handler

## Tests SQL request validation operation
#
class SQL_Validation_Test(unittest.TestCase):

    # Pattern 2
    def validate_select_zero(self):
        self.REQ_HANDLER = Request_Handler()

        self.select_pattern_1 = r"SELECT (.+?) FROM ([\w]+) WHERE (.+)"
        self.select_pattern_2 = r"SELECT (.+?) FROM ([\w]+)"

        pattern = self.REQ_HANDLER.validate_request("SELECT * FROM users")
        self.assertEqual(pattern, self.select_pattern_2)

    # Pattern 2
    def validate_select_one(self):
        pattern = self.REQ_HANDLER.validate_request("SELECT field FROM users")
        self.assertEqual(pattern, self.select_pattern_2)
    
    # Pattern 1
    def validate_select_wrong_one(self):
        pattern = self.REQ_HANDLER.validate_request("SELECT field FROM users WHERE id = 1")
        self.assertEqual(pattern, self.select_pattern_1)

    # None
    def validate_select_wrong_two(self):
        pattern = self.REQ_HANDLER.validate_request("* SELECT FROM users")
        self.assertIsNone(pattern)

    # None
    def validate_insert(self):
        pattern = self.REQ_HANDLER.validate_request("INSERT INTO users ('efe') VALUES ('efe')")
        self.assertIsNone(pattern)

    # None
    def validate_update(self):
        pattern = self.REQ_HANDLER.validate_request("UPDATE one SET field = 'efe'")
        self.assertIsNone(pattern)
    
    # None
    def validate_delete(self):
        pattern = self.REQ_HANDLER.validate_request("delete from users where id = 1")
        self.assertIsNone(pattern)
