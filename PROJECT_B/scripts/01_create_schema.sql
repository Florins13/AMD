--#############
--# Exercise 3
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

-------------------------------
-- create the relational schema
-------------------------------
DROP TABLE IF EXISTS TRACK;

CREATE TABLE TRACK
(
  tracking_record_id BIGINT NOT NULL,
  date_time          TIMESTAMP WITHOUT TIME ZONE NOT NULL,
  user_gui           VARCHAR,
  campaign_id        VARCHAR,
  product_gui        VARCHAR,
  company            VARCHAR,
  link               VARCHAR,
  tracking_id        VARCHAR,
  meio               VARCHAR,
  ip                 VARCHAR,
  browser            VARCHAR,
  session_id         VARCHAR,
  referer            VARCHAR,
  cookie_id          VARCHAR
);

-------------------------------
-- entity integrity constraints
-------------------------------
ALTER TABLE TRACK
ADD CONSTRAINT pk_track
PRIMARY KEY (tracking_record_id);

ALTER TABLE TRACK
ADD CONSTRAINT uk_track
UNIQUE (tracking_record_id);
