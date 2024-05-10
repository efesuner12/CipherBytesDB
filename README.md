# CipherBytesDB
**CipherBytesDB** is a database encryption solution for small to medium size organisations that provides confidentiality for MySQL databases in the cloud and on-premise. 

Through a wide ranged set of encryption models combined with state-of-art encryption practices, this application provides data security on multiple levels; data-at-rest, data-in-use and data-in-transit, while targetting intruders and insiders by offering an encryption-based access control mechanism, enabling a comprehensive and secure access management of data subsets.

Furthermore, it presents a data retrieval API that is designed for querying encrypted datasets, aiming to seamlessly integrate into existing database workflows without compromising efficiency.

Developed as the undergraduate final year project @ The University of Birmingham

## Pre-requisites
- MySQL should already be installed on the host that will run the application 
- The External Key Management System host should be allocated with a static IP address
- A static IP address should be allocated to the application host
- The firewall should allow incoming and outgoing requests on port 3306/tcp, 80/tcp and 443/tcp on the application host

## Setup
**To setup the application please follow the below steps:**
- git clone git@git.cs.bham.ac.uk:projects-2023-24/ses907.git
- cd ses907
- bash setup.sh

**You'd also need to setup the external key management system for the full experience. To do so, follow the steps in the ekms/ directory.**

**TLS Certificate Setup for the Data Retrieval API**
- Change the TLS certificate path in app/api/common/config.py
- Change the TLS private key path in app/api/common/config.py

**Once all setups are completed, follow below steps to run the application:**
- source venv/bin/activate
- python3 main.py

## Data Retrieval API Requests
**Authentication:** <br />
curl -i -X POST -H "Content-Type: application/json" -d '{"host":"<host_address>","database":"<database_name>","username":"<your_username>","password":"<your_password>"}' http://127.0.0.1:8080/api/v1/auth

**Plaintext Requests:** <br />
SELECT * FROM one <br />
curl -i -X GET -H "Content-Type: application/json" -d '{"token":"<your_token>"}' http://127.0.0.1:8080/api/v1/requests/SELECT%20*%20FROM%20one

SELECT * FROM one WHERE id = 1 <br />
curl -i -X GET -H "Content-Type: application/json" -d '{"token":"<your_token>"}' http://127.0.0.1:8080/api/v1/requests/SELECT%20*%20FROM%20one%20WHERE%20id%20=%201

SELECT * FROM one WHERE test2_id IS NULL <br />
curl -i -X GET -H "Content-Type: application/json" -d '{"token":"<your_token>"}' http://127.0.0.1:8080/api/v1/requests/SELECT%20*%20FROM%20one%20WHERE%20test2_id%20IS%20NULL

SELECT field_2, field_3 FROM one <br />
curl -i -X GET -H "Content-Type: application/json" -d '{"token":"<your_token>"}' http://127.0.0.1:8080/api/v1/requests/SELECT%20field_2,%20field_3%20FROM%20one

SELECT field_2, field_3 FROM one WHERE id = 1 AND field = "test_1" <br />
curl -i -X GET -H "Content-Type: application/json" -d '{"token":"<your_token>"}' http://127.0.0.1:8080/api/v1/requests/SELECT%20field_2,%20field_3%20FROM%20one%20WHERE%20id%20=%201%20AND%20field%20=%20%27test_1%27

## Testing
**To setup test databases, run the following commands in mysql:**
- source "<path_to_app_directory>"/tests/test-db.sql
- source "<path_to_app_directory>"/tests/football-db.sql

**To run the automated unit tests, run the following commands:**
- source venv/bin/activate
- python3 run_tests.py
