--CREACION DE TABLA
CREATE OR REPLACE EXTERNAL TABLE `ex-final-481401.bronce_processed.flight_delay_ext`
OPTIONS (
  format = 'CSV',
  uris = ['gs://bronce_processed/flight_delay_clean_csv/*.csv'],
  skip_leading_rows = 1,
  allow_quoted_newlines = TRUE
);

CREATE OR REPLACE TABLE `ex-final-481401.bronce_processed.flight_delay` AS
SELECT * FROM `ex-final-481401.bronce_processed.flight_delay_ext`;
