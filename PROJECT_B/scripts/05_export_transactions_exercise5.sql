--#############
--# Exercise 5 - Export Transactions for Market-Basket Analysis
--# Based on PRACTICE_7 scripts
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

--==========================
-- Output file path
-- Format: TRANSACTION_ID;PRODUCT_ID
-- Where TRANSACTION_ID can be session_id or cookie_id
-- Output to PROJECT_B root directory
--==========================
\set filePath '../transactions_filtered.txt'
--==========================

--==============================
-- Export to text data file
--==============================
-- Important: "\o" psql statement redirects STDOUT to a file
-- This uses client credentials instead of server credentials
\o :filePath

--==============================
-- Export transactions from filtered view
-- Format: TRANSACTION_ID;PRODUCT_ID
-- Using session_id as TRANSACTION_ID for market-basket analysis
--==============================

COPY ( 
  SELECT session_id, product_gui 
  FROM v_export_filtered 
  ORDER BY cookie_id, session_id, product_gui 
)
TO STDOUT
WITH ( FORMAT CSV, HEADER FALSE, DELIMITER ';' )
;

-- Close output redirection
\o

--==============================
-- Show export statistics
--==============================

\echo ''
\echo '=========================================='
\echo 'EXPORT COMPLETED: Exercise 5'
\echo '=========================================='
\echo 'Output file: transactions_filtered.txt'
\echo 'Format: TRANSACTION_ID;PRODUCT_ID'
\echo '=========================================='

-- Count exported records
SELECT COUNT(*) AS total_exported_transactions
FROM v_export_filtered
;

-- Count unique transactions (sessions)
SELECT COUNT(DISTINCT session_id) AS unique_transaction_ids
FROM v_export_filtered
;

-- Count unique products
SELECT COUNT(DISTINCT product_gui) AS unique_product_ids
FROM v_export_filtered
;

-- Show sample of exported data
\echo ''
\echo '=========================================='
\echo 'SAMPLE: First 10 transactions'
\echo '=========================================='
SELECT session_id AS transaction_id, product_gui AS product_id
FROM v_export_filtered
ORDER BY session_id, product_gui
LIMIT 10
;
