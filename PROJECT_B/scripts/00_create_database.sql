--#############
--# Exercise 3
--# Create PostgreSQL database
--#############

--==============
-- DB connection as postgres user
--==============
\set dataBase db_project_b
;
\set userName postgres
;

-- Connect to default database to create new one
\connect postgres :userName
;

-- Drop database if exists
DROP DATABASE IF EXISTS :dataBase;

-- Create database
CREATE DATABASE :dataBase
WITH 
  OWNER = :userName
  ENCODING = 'UTF8'
  CONNECTION LIMIT = -1;
