CREATE DATABASE IF NOT EXISTS silver_db;

CREATE TABLE silver_db.silver_consumo_mensual
WITH (
  external_location = 's3://lds-s3-bucket-demo/silver/consumo_mensual/',
  format = 'PARQUET',
  write_compression = 'SNAPPY'
) AS
SELECT
  id_suministro,
  id_medidor,
  anio_mes,
  energia_total_kwh,
  demanda_max_kw,
  n_registros,
  n_registros_error,
  n_registros_error * 1.0 / NULLIF(n_registros, 0) AS pct_registros_error
FROM bronze_db.bronze_acumulado;
