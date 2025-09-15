#!/bin/bash
dataBase="postgres"
userName="florin"
portNumber=5432

psql -h localhost -p "$portNumber" -d "$dataBase" -U "$userName" -f "$1"
