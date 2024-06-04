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

# Creates the cipherbytesdb database and its tables
function createDatabase()
{
    printf "[+] Creating the cipherbytesdb database and the tables...\n"

    local SQL_COMMANDS="
    DROP DATABASE IF EXISTS cipherbytesdb;
    CREATE DATABASE cipherbytesdb;
    USE cipherbytesdb;
    CREATE TABLE IF NOT EXISTS admin (
        id INT AUTO_INCREMENT UNIQUE,
        username VARCHAR(32) NOT NULL UNIQUE,
        password VARCHAR(160) NOT NULL UNIQUE,
        PRIMARY KEY(id)
    );
    CREATE TABLE IF NOT EXISTS connected_dbs (
        id INT AUTO_INCREMENT UNIQUE,
        host VARCHAR(40) NOT NULL,
        db_name VARCHAR(50) NOT NULL,
        db_nickname VARCHAR(50) NOT NULL,
        username VARCHAR(32) NOT NULL,
        password VARCHAR(255) NOT NULL UNIQUE,
        key_rotation_interval ENUM('Yearly', 'Monthly', 'Weekly', 'Daily') NOT NULL DEFAULT 'Monthly',
        PRIMARY KEY(id)
    );
    CREATE TABLE IF NOT EXISTS table_encryption_model (
        id INT AUTO_INCREMENT UNIQUE,
        host_identifier VARCHAR(100) NOT NULL,
        table_name VARCHAR(100) NOT NULL,
        encryption_model ENUM('0', '1', '2', '3') NOT NULL,
        detail VARCHAR(512),
        PRIMARY KEY(id, host_identifier)
    );
    CREATE TABLE IF NOT EXISTS encrypted_column_data (
        id INT AUTO_INCREMENT UNIQUE,
        host_identifier VARCHAR(100) NOT NULL,
        table_name VARCHAR(100) NOT NULL,
        column_name VARCHAR(512) NOT NULL,
        old_data_type VARCHAR(512) NOT NULL,
        old_data_length INT,
        default_constraint VARCHAR(512),
        auto_inc_constraint VARCHAR(512),
        not_null_constraint ENUM('True', 'False') NOT NULL DEFAULT 'False',
        check_constraint VARCHAR(512),
        foreign_key_constraint VARCHAR(512),
        unique_constraint VARCHAR(512),
        PRIMARY KEY(id, host_identifier)
    );
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT UNIQUE,
        host_identifier VARCHAR(100) NOT NULL,
        username VARCHAR(32) NOT NULL,
        user_privilage ENUM('admin', 'user') NOT NULL,
        PRIMARY KEY(id)
    );
    CREATE TABLE IF NOT EXISTS access_controls (
        id INT AUTO_INCREMENT UNIQUE,
        host_identifier VARCHAR(100) NOT NULL,
        table_name VARCHAR(100) NOT NULL,
        user_id INT NOT NULL,
        key_id INT NOT NULL,
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

# Creates the cipherbytesdb mysql user and grants it all privilages on cipherbytesdb
# and select privilage on mysql.user
function createDBUser()
{
    printf "[+] Creating the cipherbytesdb database user...\n"
    printf "[+] Granting it full access to cipherbytesdb database...\n"

    local SQL_USER_CREATE="CREATE USER 'cbdb_user'@'localhost' IDENTIFIED BY 'Somebody w1ll be able to overcome any encryption technique you use!';"
    local SQL_PERMISSIONS="
    GRANT ALL PRIVILEGES ON cipherbytesdb.* TO 'cbdb_user'@'localhost';
    GRANT SELECT on mysql.user TO 'cbdb_user'@'localhost';
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

# Selects the users and revokes their privilages in cipherbytesdb database
# if they are not in the allowed users list
function revokePermissions()
{
    printf "[+] Revoking all permissions to cipherbytesdb database except of root, debian-sys-maint, mysql.infoschema, mysql.session, mysql.sys and cbdb_user...\n"

    local SQL_USERS="SELECT User, Host FROM mysql.user;"

    trap 'handleMySQLError' ERR
    result=$(mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -D "mysql" -s -N -e "$SQL_USERS")
    trap - ERR

    ALLOWED_USERS=("root" "debian-sys-maint" "mysql.infoschema" "mysql.session" "mysql.sys" "cbdb_user")

    echo "$result" | while read -r user host; do
        if [[ ! " ${ALLOWED_USERS[@]} " =~ " $user " ]]; then           
            local SQL_REVOKE="REVOKE ALL PRIVILEGES ON cipherbytesdb.* FROM '$user'@'$host';"

            trap 'handleMySQLError' ERR
            mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$SQL_REVOKE"
            trap - ERR
        fi
    done

    printf "Done.\n\n"
}

# Hashes and salts the password input
function hash() 
{
    local password=$1
    local salt=$(openssl rand -hex 16)
    local hashedPassword=$(python3 -c "import hashlib; print(hashlib.pbkdf2_hmac('sha512', b'$password', bytes.fromhex('$salt'), 100000).hex())")

    local result="$salt$hashedPassword"
    echo "$result"
}

# Validates the username input
function validUsername()
{
    local username=$1

    for (( i=0; i<${#username}; i++ )); 
    do
        char="${username:i:1}"

        if [[ $char =~ [[:upper:]] ]] || [[ $char == " " ]]; 
        then
            return 1
        fi
    done

    return 0
}

# Gets user input and creates the admin user in the database
function createAdmin()
{
    local isValid=1

    while [ $isValid -eq 1 ]
    do
        printf "Enter admin username: "
        read username

        validUsername "$username"
        isValid=$?

        if [[ $isValid -eq 1 ]];
        then
            printf "Please enter a valid username\n\n"
        fi
    done

    printf "Enter admin password: "
    read -s password

    local result=$(hash "$password")
    printf "\n[+] Password Hashed.\n"

    local SQL_COMMANDS="
    USE cipherbytesdb;
    INSERT INTO admin (username, password) VALUES ('$username', '$result');"

    printf "[+] Inserting into the admin table...\n"

    trap 'handleMySQLError' ERR
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -e "$SQL_COMMANDS"
    trap - ERR

    printf "Done.\n\n"
}

# Encrypts the given plaintext
function encrypt()
{
    local filePath=$1
    local plaintext=$2
    local userPassword=$3

    # install crypto module
    #pip3 install "cryptography==41.0.7"

    # encrypt
    python3 -c "import app.operation.cryptography.file_encryption as file_encryptor; file_encryptor.encrypt_file_data('$filePath', '$plaintext', '$userPassword')"

    # uninstall crypto module
    #pip3 uninstall "cryptography==41.0.7"    
}

# Creates the directory and encrypts the db configs and changes the file permissions
function storeDatabaseConfigs()
{
    local userPassword=$1

    printf "[+] Creating the database config file...\n"

    local folderPath="$HOME/.config/cipherbytesdb"

    printf "[+] Creating $folderPath...\n"
    mkdir -p "$folderPath"
    chmod a-rwx "$folderPath"
    chmod u+rwx "$folderPath"
    printf "Done.\n"

    local JSON="{\"host\":\"127.0.0.1\",\"database\":\"cipherbytesdb\",\"user\":\"cbdb_user\",\"password\":\"Somebody w1ll be able to overcome any encryption technique you use!\"}"

    local filePath="$HOME/.config/cipherbytesdb/db_configs.conf"

    # Print here otherwise print txt will be written into config file as well
    printf "[+] Encrypting the database configs...\n"

    encrypt "$filePath" "$JSON" "$userPassword"

    printf "Done.\n"

    chmod a-rwx "$filePath"
    chmod u+rw "$filePath"

    printf "Done.\n\n"
}

# Encrypts the EKMS db configs and changes the file permissions
function storeEKMSDatabaseConfigs()
{
    local userPassword=$1

    local folderPath="$HOME/.config/cipherbytesdb"

    printf "[+] Creating the EKMS database config file...\n"

    printf "Enter the IP address of the EKMS: "
    read ekmsIP

    local JSON="{\"host\":\"$ekmsIP\",\"database\":\"cipherbytesdb_kms\",\"user\":\"cbdb_kms_user\",\"password\":\"Wh3n !n doubt use brute force\"}"

    local filePath="$folderPath/ekms_db_configs.conf"

    # Print here otherwise print txt will be written into config file as well
    printf "[+] Encrypting the database configs...\n"

    encrypt "$filePath" "$JSON" "$userPassword"

    printf "Done.\n"
    
    chmod a-rwx "$filePath"
    chmod u+rw "$filePath"

    printf "Done.\n\n"
}

# Handles errors raised by Python3 installation
function handlePythonInstallError()
{
    printf "\nAn unexpected error has occured during the installation of Python3.\nExiting...\n\n"
    exit 1
}

# Installs Python3
function installPython()
{
    printf "[+] Installing Python3...\n"

    trap 'handlePythonInstallError' ERR
    sudo apt-get install python3
    trap - ERR

    printf "Done.\n\n"
}

# Checks if Python3 is installed with python3 -v command
function isPythonInstalled()
{
    printf "[+] Checking if Python is installed...\n"

    if ! command -v python3 &> /dev/null;
    then
        printf "Python is not installed.\n"
        installPython
    fi

    printf "Done.\n\n"
}

# Handles errors raised by Python3.*-venv installation
function handlePythonVenvInstallError()
{
    printf "\nAn unexpected error has occured during the installation of Python3-venv.\nExiting...\n\n"
    exit 1
}

# Installs Python3-venv with specific version number
function installPythonVenv()
{
    printf "Installing Python3-venv...\n"

    trap 'handlePythonVenvInstallError' ERR
    
    pythonVersion=$(python3 --version 2>&1 | awk '{split($2, a, "."); print a[1]"."a[2]}')
    packageName="python${pythonVersion}-venv"
    sudo apt install "$packageName"

    trap - ERR

    printf "Done.\n\n"
}

# Checks if Python3.*-venv is installed 
function isPythonVenvInstalled()
{
    printf "[+] Checking if Python3.*-venv is installed...\n"

    if ! apt list --installed | grep python3.*-venv; then
        printf "Python3.*-venv is not installed.\n"
        installPythonVenv
    fi

    printf "Done.\n\n"
}

# Handles errors raised by Python3-pip installation
function handlePythonPipInstallError()
{
    printf "\nAn unexpected error has occured during the installation of Python3-pip.\nExiting...\n\n"
    exit 1
}

# Installs Python3-pip
function installPythonPip()
{
    printf "Installing Python3-pip...\n"

    trap 'handlePythonPipInstallError' ERR
    sudo apt install python3-pip
    trap - ERR

    printf "Done.\n\n"
}

# Checks if Python3.*-pip is installed
function isPythonPipInstalled()
{
    printf "[+] Checking if Python3.*-pip is installed...\n"

    if ! apt list --installed | grep python3.*-pip; then
        printf "Python3.*-pip is not installed.\n"
        installPythonPip
    fi

    printf "Done.\n\n"
}

clear
printf "Setup CipherBytesDB\n\n"

isMySQLInstalled
mySQLInstalled=$?

if [[ $mySQLInstalled ]];
then
    printf "Done.\n\n"

    createDatabase
    createDBUser
    revokePermissions
    createAdmin

    storeDatabaseConfigs "$password"
    storeEKMSDatabaseConfigs "$password"

    printf "[+] Creating the cipherbytesdb folder...\n"
    mkdir ~/.cipherbytesdb/
    chmod a-rwx ~/.cipherbytesdb/
    chmod u+rwx ~/.cipherbytesdb/
    printf "Done.\n\n"

    isPythonInstalled

    isPythonVenvInstalled

    printf "[+] Creating the virtual environment...\n"
    python3 -m venv venv
    printf "Done.\n\n"

    printf "[+] Activating the virtual environment...\n"
    source venv/bin/activate
    printf "Done.\n\n"

    isPythonPipInstalled

    printf "[+] Installing requirements...\n"
    pip3 install -r requirements.txt
    printf "Done.\n\n"

    printf "[+] Installing Python Tkinter...\n"
    sudo apt-get install python3-tk
    printf "Done.\n\n"
fi
