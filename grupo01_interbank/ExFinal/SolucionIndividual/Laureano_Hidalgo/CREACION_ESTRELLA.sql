-- 0) Dataset PLATA 
CREATE SCHEMA IF NOT EXISTS `ex-final-481401.plata`
OPTIONS(location = "us-east1");


-- Fuente
WITH src AS (
  SELECT * FROM `ex-final-481401.bronce_processed.flight_delay`
)

-- 1) DIM_DATE
CREATE OR REPLACE TABLE `ex-final-481401.plata.dim_date` AS
SELECT DISTINCT
  CAST(FORMAT_DATE('%Y%m%d', DATE(date)) AS INT64) AS date_key,
  DATE(date) AS date,
  EXTRACT(YEAR  FROM DATE(date)) AS year,
  EXTRACT(MONTH FROM DATE(date)) AS month,
  EXTRACT(DAY   FROM DATE(date)) AS day,
  SAFE_CAST(dayofweek AS INT64) AS dayofweek
FROM src
WHERE date IS NOT NULL;

-- 2) DIM_CARRIER
CREATE OR REPLACE TABLE `ex-final-481401.plata.dim_carrier` AS
SELECT DISTINCT
  ABS(FARM_FINGERPRINT(uniquecarrier)) AS carrier_key,
  uniquecarrier,
  airline
FROM src
WHERE uniquecarrier IS NOT NULL;

-- 3) DIM_AIRCRAFT
CREATE OR REPLACE TABLE `ex-final-481401.plata.dim_aircraft` AS
SELECT DISTINCT
  ABS(FARM_FINGERPRINT(tailnum)) AS aircraft_key,
  tailnum
FROM src
WHERE tailnum IS NOT NULL;

-- 4) DIM_AIRPORT (union origen + destino)
CREATE OR REPLACE TABLE `ex-final-481401.plata.dim_airport` AS
WITH airports AS (
  SELECT DISTINCT origin AS airport_code, org_airport  AS airport_name FROM src
  UNION DISTINCT
  SELECT DISTINCT dest   AS airport_code, dest_airport AS airport_name FROM src
)
SELECT
  ABS(FARM_FINGERPRINT(airport_code)) AS airport_key,
  airport_code,
  airport_name
FROM airports
WHERE airport_code IS NOT NULL;

-- 5) DIM_FLIGHT (carrier + flightnum)
CREATE OR REPLACE TABLE `ex-final-481401.plata.dim_flight` AS
SELECT DISTINCT
  ABS(FARM_FINGERPRINT(CONCAT(uniquecarrier, '|', flightnum))) AS flight_key,
  uniquecarrier,
  flightnum
FROM src
WHERE uniquecarrier IS NOT NULL AND flightnum IS NOT NULL;

-- 6) FACT_FLIGHT_DELAY
CREATE OR REPLACE TABLE `ex-final-481401.plata.fact_flight_delay` AS
SELECT
  CAST(FORMAT_DATE('%Y%m%d', DATE(s.date)) AS INT64) AS date_key,

  ABS(FARM_FINGERPRINT(s.uniquecarrier)) AS carrier_key,
  ABS(FARM_FINGERPRINT(CONCAT(s.uniquecarrier, '|', s.flightnum))) AS flight_key,
  ABS(FARM_FINGERPRINT(s.tailnum)) AS aircraft_key,

  ABS(FARM_FINGERPRINT(s.origin)) AS origin_airport_key,
  ABS(FARM_FINGERPRINT(s.dest))   AS dest_airport_key,

  parse_hhmm(CAST(s.deptime    AS STRING)) AS dep_time,
  parse_hhmm(CAST(s.arrtime    AS STRING)) AS arr_time,
  parse_hhmm(CAST(s.crsarrtime AS STRING)) AS crs_arr_time,

  SAFE_CAST(s.actualelapsedtime AS INT64) AS actual_elapsed_time,
  SAFE_CAST(s.crselapsedtime    AS INT64) AS crs_elapsed_time,
  SAFE_CAST(s.airtime           AS INT64) AS air_time,

  SAFE_CAST(s.arrdelay          AS INT64) AS arr_delay,
  SAFE_CAST(s.depdelay          AS INT64) AS dep_delay,

  SAFE_CAST(s.distance          AS INT64) AS distance,
  SAFE_CAST(s.taxiin            AS INT64) AS taxi_in,
  SAFE_CAST(s.taxiout           AS INT64) AS taxi_out,

  SAFE_CAST(s.carrierdelay      AS INT64) AS carrier_delay,
  SAFE_CAST(s.weatherdelay      AS INT64) AS weather_delay,
  SAFE_CAST(s.nasdelay          AS INT64) AS nas_delay,
  SAFE_CAST(s.securitydelay     AS INT64) AS security_delay,
  SAFE_CAST(s.lateaircraftdelay AS INT64) AS late_aircraft_delay,

  SAFE_CAST(s.cancelled AS INT64) = 1 AS cancelled,
  SAFE_CAST(s.diverted  AS INT64) = 1 AS diverted,
  CAST(s.cancellationcode AS STRING) AS cancellation_code,

  s._source_path,
  s._ingestion_ts
FROM `ex-final-481401.bronce_processed.flight_delay` s
WHERE s.date IS NOT NULL;
