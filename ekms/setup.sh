#!/bin/bash

# 0 == true
# 1 == false

MYSQL_USER="root"
MYSQL_PASSWORD=""

# Checks if MySQL is installed with mysql -v command
function isMySQLInstalled()
{
    printf "[+] Checking if MySQL is installed...\n"

    if ! command -v mysql &> /dev/null; 
    then
        printf "MySQL is not installed. Please install MySQL before running this script.\n"
        exit 1
    fi

    return 0
}

# Handles errors raised by MySQL operations
function handleMySQLError()
{
    printf "\nAn unexpected error has occured during the MySQL operation.\nExiting...\n\n"
    exit 1
}

# Creates the cipherbytesdb database and the admin table
function createDatabase()
{
    printf "[+] Creating the cipherbytesdb_kms database and the tables...\n"

    local SQL_COMMANDS="
    DROP DATABASE IF EXISTS cipherbytesdb_kms;
    CREATE DATABASE cipherbytesdb_kms;
    USE cipherbytesdb_kms;
    CREATE TABLE IF NOT EXISTS encryption_keys (
        id INT AUTO_INCREMENT UNIQUE,
        encryption_priv_key VARCHAR(256) NOT NULL UNIQUE,
        encryption_pub_key VARCHAR(256) NOT NULL UNIQUE,
        creation_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        expiration_datetime DATETIME NOT NULL,
        encryption_metadata VARCHAR(128) NOT NULL UNIQUE,
        PRIMARY KEY(id)
    );
    "

    printf "Enter your MySQL password: "
    read -s MYSQL_PASSWORD
    
    printf "\n"

    trap 'handleMySQLError' ERR
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$SQL_COMMANDS"
    trap - ERR

    printf "Done.\n\n"
}

# Creates the cipherbytesdb mysql user and grants it all privilages on cipherbytesdb_kms
# 
function createDBUser()
{
    printf "[+] Creating the cipherbytesdb_kms remote database user...\n"
    printf "[+] Granting it full access to cipherbytesdb_kms database...\n"

    printf "Enter the IP address of the application host: "
    read appIP

    local SQL_USER_CREATE="CREATE USER 'cbdb_kms_user'@'$appIP' IDENTIFIED BY 'Wh3n !n doubt use brute force';"
    local SQL_PERMISSIONS="
    GRANT ALL PRIVILEGES ON cipherbytesdb_kms.* TO 'cbdb_kms_user'@'$appIP';
    FLUSH PRIVILEGES;
    "

    trap 'handleMySQLError' ERR
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$SQL_USER_CREATE"
    trap - ERR

    trap 'handleMySQLError' ERR
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$SQL_PERMISSIONS"
    trap - ERR

    printf "Done.\n\n"
}

# Selects the users and revokes their privilages in cipherbytesdb_kms database
# if they are not in the allowed users list
# (cbdb_user is an exception as it already has no access set otherwise MySQL error)
function revokePermissions()
{
    printf "[+] Revoking all permissions to cipherbytesdb_kms database except of root, debian-sys-maint, mysql.infoschema, mysql.session, mysql.sys and cbdb_kms_user...\n"

    local SQL_USERS="SELECT User, Host FROM mysql.user;"

    trap 'handleMySQLError' ERR
    result=$(mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D "mysql" -s -N -e "$SQL_USERS")
    trap - ERR

    ALLOWED_USERS=("root" "debian-sys-maint" "mysql.infoschema" "mysql.session" "mysql.sys" "cbdb_kms_user" "cbdb_user")

    echo "$result" | while read -r user host; do
        if [[ ! " ${ALLOWED_USERS[@]} " =~ " $user " ]]; then           
            local SQL_REVOKE="REVOKE ALL PRIVILEGES ON cipherbytesdb_kms.* FROM '$user'@'$host';"

            trap 'handleMySQLError' ERR
            mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$SQL_REVOKE"
            trap - ERR
        fi
    done

    printf "Done.\n\n"
}

clear
printf "Setup CipherBytesDB - External Key Management System\n\n"

isMySQLInstalled
mySQLInstalled=$?

if [[ $mySQLInstalled ]];
then
    printf "Done.\n\n"

    createDatabase
    createDBUser
    revokePermissions
fi
