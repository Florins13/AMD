--#############
--# Exercise 4 - Filter Relevant Data for Market-Basket Analysis
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

--=============================================================================
-- Exercise 4: Generate subset of most relevant data
-- Filter visitors with 5 <= number_of_sessions <= 30
--=============================================================================

-- Drop existing view if it exists
DROP VIEW IF EXISTS v_export_filtered;

-- Create filtered view for market-basket analysis
-- This view contains only events from visitors with 5 to 30 sessions
-- Also filters out invalid product_gui values
CREATE VIEW v_export_filtered( cookie_id, session_id, product_gui )
AS
SELECT T1.cookie_id, session_id, product_gui
FROM ( SELECT *
       FROM v_cookie_number_of_sessions
       WHERE number_of_sessions >= 5 AND number_of_sessions <= 30 ) AS T1
     INNER JOIN
     track AS T2
     ON ( T1.cookie_id = T2.cookie_id )
WHERE product_gui NOT IN ( 'open', 'home', 'Spy', 'Tecnologia', 'Divertimento', 'Jogos',
                           '/customer/account/login/', '/customer/account/forgotpassword/',
                           '/customer/account/create/' )
  AND product_gui NOT LIKE '/%'
  AND product_gui NOT LIKE '/catalog/%'
;
-- Note: ORDER BY is commented for performance (will be used during export)
-- ORDER BY cookie_id, session_id, product_gui;


--=============================================================================
-- Statistics for Exercise 4: Filtered Dataset
--=============================================================================

-- Count total events in filtered dataset
SELECT COUNT(*) AS total_filtered_events
FROM v_export_filtered
;

-- Count unique visitors in filtered dataset
SELECT COUNT(DISTINCT cookie_id) AS total_filtered_visitors
FROM v_export_filtered
;

-- Count unique sessions in filtered dataset
SELECT COUNT(DISTINCT session_id) AS total_filtered_sessions
FROM v_export_filtered
;

-- Count unique products in filtered dataset
SELECT COUNT(DISTINCT product_gui) AS total_filtered_products
FROM v_export_filtered
;

-- Show distribution of sessions for filtered visitors
SELECT 
  T1.number_of_sessions,
  COUNT(*) AS number_of_visitors,
  SUM(T1.number_of_events) AS total_events
FROM v_cookie_number_of_sessions AS T1
WHERE T1.number_of_sessions >= 5 AND T1.number_of_sessions <= 30
GROUP BY T1.number_of_sessions
ORDER BY T1.number_of_sessions ASC
;

-- Sample of filtered data (first 20 rows)
\echo ''
\echo '=========================================='
\echo 'SAMPLE: First 20 filtered events'
\echo '=========================================='
SELECT cookie_id, session_id, product_gui
FROM v_export_filtered
ORDER BY cookie_id, session_id
LIMIT 20
;
