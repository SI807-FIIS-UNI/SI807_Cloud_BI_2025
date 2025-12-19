CREATE TABLE lds_silver.silver_asign_tarifa
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/silver/asignacion_tarifa/'
) AS
SELECT
    a.id_asignacion_tarifa,
    a.id_suministro,
    a.id_tarifa
FROM lds_bronze.bronze_asig_tarifa a;
