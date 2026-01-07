#!/bin/bash
# [PTS: ADAPT]
# PostgreSQL bin path (adjust if needed)
# psqlPath="/usr/bin"  # Usually psql is already in PATH on Linux

# Database, Username and Port
dataBase="postgres"
userName="postgres"
portNumber=5432

#________________________________________________________________________
# Connect to database and execute the instructions within psqlFile
# psql -h host -p port -d database -U user -f psqlFile
# (cf. postgresql-9.6-A4.pdf)
#________________________________________________________________________
psql -h localhost -p $portNumber -d $dataBase -U $userName -f "$1"
