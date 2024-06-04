# CipherBytesDB - External Key Management System

**Pre-requisites:**
- A static IP address should be allocated to the host
- MySQL should already be installed on the host
- MySQL should be configured to allow remote connections:
    - The bind IP address in the MySQL configuration file should be changed
    - The remote MySQL user will be created as a part of the setup script
- The firewall should allow incoming and outgoing requests on port 3306/tcp - We recommend creating a rule specific to the application host

**To setup the application please follow the below steps:**
- git clone git@git.cs.bham.ac.uk:projects-2023-24/ses907.git
- cd ses907/ekms
- bash setup.sh

**Once the setup is completed, the EKMS is ready to be used**
