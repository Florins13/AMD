--#############
--# Exercise 3 - Aggregated Views
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

---------------------------------
-- Drop existing views
---------------------------------
DROP VIEW IF EXISTS v_export;
DROP VIEW IF EXISTS v_number_of_events_per_session_number_of_cookies;
DROP VIEW IF EXISTS v_number_of_cookies_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_number_of_sessions;
DROP VIEW IF EXISTS v_cookie_session_number_of_events;
---------------------------------


--=============================================================================
-- 1. TOTAL NUMBER OF EVENTS (January 2012)
--=============================================================================
SELECT COUNT(*) as totalEvents_JAN_2012
FROM track
;


--=============================================================================
-- 2. TOTAL NUMBER OF DISTINCT VISITORS (cookie_id cardinality)
--=============================================================================
SELECT COUNT(*) AS totalNumberOfVisitors_cookie_id_JAN_2012
FROM (SELECT DISTINCT cookie_id FROM track) AS T
;


--=============================================================================
-- 3. Aggregate cookies and sessions - get total number of events per session
--=============================================================================
CREATE VIEW v_cookie_session_number_of_events
( cookie_id, session_id, number_of_events_per_session )
AS
SELECT
  cookie_id,
  session_id,
  COUNT(*) AS number_of_events_per_session
FROM track
GROUP BY
  cookie_id,
  session_id
ORDER BY
  number_of_events_per_session DESC,
  cookie_id,
  session_id
;


--=============================================================================
-- 4. Aggregate cookie - get total number of sessions (for each cookie)
--=============================================================================
CREATE VIEW v_cookie_number_of_sessions
( cookie_id, number_of_sessions, number_of_events )
AS
SELECT
  cookie_id,
  COUNT(*) AS number_of_sessions,
  SUM(number_of_events_per_session) AS number_of_events
FROM v_cookie_session_number_of_events
GROUP BY
  cookie_id
ORDER BY
  number_of_events DESC
;


--=============================================================================
-- 5. DISTRIBUTION: number-of-visitors vs number-of-sessions
--=============================================================================
CREATE VIEW v_number_of_cookies_number_of_sessions
( numberOfVisitors, numberOfSessions )
AS
SELECT
  COUNT(cookie_id) AS numberOfVisitors,
  number_of_sessions AS numberOfSessions
FROM v_cookie_number_of_sessions
GROUP BY
  number_of_sessions
ORDER BY
  number_of_sessions ASC
;

SELECT *
FROM v_number_of_cookies_number_of_sessions
;


--=============================================================================
-- 6. DISTRIBUTION: number-of-events-per-session vs number-of-visitors
--=============================================================================
CREATE VIEW v_number_of_events_per_session_number_of_cookies
( numberOfEventsPerSession, numberOfVisitors )
AS
SELECT
  number_of_events_per_session AS numberOfEventsPerSession,
  COUNT(DISTINCT cookie_id) AS numberOfVisitors
FROM v_cookie_session_number_of_events
GROUP BY
  number_of_events_per_session
ORDER BY
  number_of_events_per_session ASC
;

SELECT *
FROM v_number_of_events_per_session_number_of_cookies
;


--=============================================================================
-- 7. VISITORS WITH EXACTLY 18 SESSIONS (for validation)
--=============================================================================
SELECT 
  cookie_id AS visitor_id,
  number_of_sessions AS numberOfSessions,
  number_of_events AS totalNumberOfEvents
FROM v_cookie_number_of_sessions
WHERE number_of_sessions = 18
ORDER BY cookie_id
;
