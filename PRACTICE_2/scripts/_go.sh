#!/bin/bash
dataBase="db_operational"
userName="postgres"
portNumber=5432

psql -h localhost -p "$portNumber" -d "$dataBase" -U "$userName" -f "$1"