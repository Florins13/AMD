--#############
--# Exercise 3
--# Import data from CSV
--#############

--==============
-- DB connection
--==============
\set dataBase db_project_b
;
\set userName postgres
;
\connect :dataBase :userName
;

-------------------------------
-- Import data from CSV
-------------------------------
\COPY track FROM '../z_dataset_JAN_updated.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ESCAPE '"');
