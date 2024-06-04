from app.db.database import Users, Access_Control_Data
from app.operation.validation import Validater
from app.operation.ekms_api import EKMS_API

class Access_Control():

    def __init__(self, db_data_pack, table_name):
        self.HOST = db_data_pack[0]
        self.DB_NAME = db_data_pack[1]

        self.TABLE_NAME = table_name

    ## Gets the created access control rules
    # from the database
    def get_ac_rules(self, error_msg):
        access_control_db = Access_Control_Data(error_msg)
        rules = access_control_db.select_rules(self.HOST, self.DB_NAME, self.TABLE_NAME)

        return rules

    ## Validates the given users
    # + Checks for duplicates and removes them
    # + Cheks if the usernames are valid
    # + Checks if the users exist
    def validate_users(self, users, error_msg):

        if users != list(dict.fromkeys(users)):
            error_msg.set("Please remove duplicates")
            return False

        validater = Validater()

        if any(not validater.valid_username(user) for user in users):
            error_msg.set("Please enter valid usernames")
            return False

        users_db = Users(error_msg)

        if any(not users_db.has_user(self.HOST, self.DB_NAME, user) for user in users):
            error_msg.set("Please enter existing users")
            return False

        return True

    ## Validates the given keys by checking
    # if they exist
    def validate_keys(self, key_ids, error_msg):
        ekms = EKMS_API(error_msg)

        if any(not ekms.has_key(key_id) for key_id in key_ids):
            error_msg.set("Please enter an existing key ID")
            return False

        return True

    ## Validates the given rules by checking users
    # and keys
    # + Checks if username or key ID fields are empty
    def validate_rules(self, rules, error_msg):
        # rules: [('username', 'key_id'), ...]

        if any(rule[0].get() == "" or rule[1].get() == "" for rule in rules):
            error_msg.set("Username and key ID fields are mandatory")
            return False

        users = [rule[0].get() for rule in rules]
        users_valid = self.validate_users(users, error_msg)
        
        key_ids = [rule[1].get() for rule in rules]
        keys_valid = self.validate_keys(key_ids, error_msg)

        return users_valid and keys_valid

    ## Adds the given rules to the database by
    # getting the user ID from the username
    def add_ac_rule(self, rules, error_msg):
        # rules: [('username', 'key_id'), ...]

        access_control_db = Access_Control_Data(error_msg)

        users_db = Users(error_msg)

        for rule in rules:
            username = rule[0].get() if type(rule[0]) != str else rule[0] 
            key_id = rule[1].get() if type(rule[1]) != int else rule[1] 

            user_id = users_db.get_user_id(self.HOST, self.DB_NAME, username)
            added = access_control_db.add_rule(self.HOST, self.DB_NAME, self.TABLE_NAME, user_id, key_id)

            if not added:
                return False

        return True

    ## Deletes the access control rule for a given user ID
    # and key ID
    def delete_ac_rule(self, user_id, key_id, error_msg):
        access_control_db = Access_Control_Data(error_msg)

        return access_control_db.delete_rule(self.HOST, self.DB_NAME, self.TABLE_NAME, user_id, key_id)

    ## Deletes all access control rules of a given
    # key ID
    def delete_ac_rules(self, key_id, error_msg):
        access_control_db = Access_Control_Data(error_msg)

        return access_control_db.delete_key_rules(self.HOST, self.DB_NAME, self.TABLE_NAME, key_id)

    ## Checks if an access control rule exists on the
    # given user ID and key ID
    def has_access(self, user_id, key_id, error_msg):
        access_control_db = Access_Control_Data(error_msg)

        return access_control_db.has_rule(self.HOST, self.DB_NAME, self.TABLE_NAME, user_id, key_id)
