import socket
import re

class Validater():

    ## Validates the username input 
    # by checking if there are any uppercase letters or spaces
    def valid_username(self, username):
        return False if any(c.isupper() or c == " " for c in username) else True

    ## Validates the host input 
    # by checking if the input can be successfully converted into its binary format
    def valid_host(self, host):
        if host == "localhost":
            return True

        # For IPv4
        try:
            socket.inet_pton(socket.AF_INET, host)  
            return True
        except socket.error:
            # For IPv6
            try:
                socket.inet_pton(socket.AF_INET6, host)  
                return True
            except socket.error:
                return False

    ## Validates the cell identifier input
    # by checking if colon is used and the number of colons
    # are higher than the number of semicolons by 1
    def valid_cell_identifier(self, cell_id):
        return True if ':' in cell_id and cell_id.count(':') - cell_id.count(';') == 1 else False

    ## Validates the incoming SQL statement
    # by checking if it starts with either
    # SELECT, INSERT INTO, UPDATE or DELETE
    def valid_sql_request(self, patterns, request):
        return next((index for index, pattern in enumerate(patterns) if re.search(pattern, request, re.IGNORECASE)), None)
