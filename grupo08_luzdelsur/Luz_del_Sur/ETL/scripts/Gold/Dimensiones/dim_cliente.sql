CREATE TABLE lds_gold.dim_cliente
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/dim_cliente/'
) AS
SELECT
    c.id_cliente,
    c.tipo_cliente,
    c.fecha_alta,
    c.estado_cliente,
    c.antiguedad_anios,
    c.tiene_email,
    c.tiene_celular,
    c.id_ubicacion
FROM lds_silver.silver_cliente c;
