#!/bin/bash

# PostgreSQL path - may need to be adjusted depending on installation
# psqlPath="/usr/bin"  # Default PostgreSQL bin location on most Linux systems

# Database, Username and Port
database="postgres"
userName="postgres"
portNumber="5432"

# Connect to database and execute the instructions within psqlFile
# psql -h host -p port -d database -U user -f psqlFile
# ${psqlPath}/psql -h localhost -p ${portNumber} -d ${database} -U ${userName} -f "$1"

psql -h localhost -p "$portNumber" -d "$database" -U "$userName" -f "$1"