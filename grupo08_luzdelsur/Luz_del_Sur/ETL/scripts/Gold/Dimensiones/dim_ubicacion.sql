CREATE TABLE lds_gold.dim_ubicacion
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/dim_ubicacion/'
) AS
SELECT
    u.id_ubicacion,
    u.distrito,
    u.zona,
    u.ubigeo
FROM lds_silver.silver_ubicacion u;
