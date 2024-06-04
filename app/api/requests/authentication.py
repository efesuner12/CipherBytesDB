from flask import request
from flask_restful import Resource
from datetime import datetime, timedelta

import jwt

from app.db.database import Users

import app.db.db_connection as db_connection
import app.operation.cryptography.hash as hasher
import app.operation.cryptography.aes as aes_encryptor

class Authentication(Resource):
    
    def __init__(self):
        self.EXPIRE_DELTA = 120

    ## Gets the master symmetric key from the EKMS
    # and the OS
    def get_master_sk(self):
        metadata = "cipherbytesdb#jwt#master"
        hashed_metadata = hasher.sha_512_hash(metadata) 
        
        master_sk, user_priv_key, user_pub_key = aes_encryptor.generate_encryption_key(hashed_metadata, "")

        return master_sk

    ## Generates the JWT
    # + Get the master symmetric key from the EKMS
    # + Calculate the expiration time
    # + Return the token - HS256
    def generate_auth_token(self, host, db_name, username, password):
        self.master_sk = self.get_master_sk()

        current = datetime.now()
        time_diff = timedelta(minutes=self.EXPIRE_DELTA)

        expire_time = current + time_diff
        expire_time = expire_time.timestamp()
        
        return jwt.encode({'host':host, 'database':db_name, 'username':username, 'password':password, 'exp':expire_time}, self.master_sk, algorithm='HS256')

    ## Validates the given JWT by checking the expiration date
    # and returns the decoded for further authorisation
    def validate_auth_token(self, token):

        if not token:
            return ("No token has been provided", 401)

        try:
            # Fetch the master symmetric key if not already
            if not hasattr(self, 'master_sk'):
                self.master_sk = self.get_master_sk()

            decoded = jwt.decode(token, self.master_sk, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return ("Token has expired", 401)
        except Exception:
            return ("Unexpected error", 500)
        
        return decoded

    ## HTTP POST
    # + Get host, database, username and password
    # + Return 400 Bad Request if one of the configs is empty or None
    # + Test connection with the given configs
    # + Check if the user exists in cbdb db
    # + Return 401 Unauthorized if can't connect or user does not exists
    # + Generate a JWT
    # + Return 200 OK with the authentication token
    def post(self):
        host = request.json.get('host')
        db_name = request.json.get('database')
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not (host and db_name and username and password):
            return "Required configurations not provided", 400

        can_connect = db_connection.test_connection(host, db_name, username, password)

        cbdb_users = Users("")
        user_exists = cbdb_users.has_user(host, db_name, username)

        if can_connect and user_exists:
            token = self.generate_auth_token(host, db_name, username, password)

            return f"Your access token is: '{token}'", 200

        return "Incorrect database configurations", 401
