CREATE TABLE lds_silver.silver_cliente
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/silver/cliente/'
) AS
SELECT
    c.id_cliente,
    UPPER(c.tipo_cliente)                  AS tipo_cliente,
    c.dni,
    c.celular,
    c.email,
    c.id_ubicacion,
    c.fecha_alta,
    UPPER(c.estado_cliente)               AS estado_cliente,
    -- antigüedad en años (al cierre 2024-12-31)
    DATE_DIFF('year', c.fecha_alta, DATE '2024-12-31') AS antiguedad_anios,
    -- flags simples
    (c.email IS NOT NULL AND c.email <> '')   AS tiene_email,
    (c.celular IS NOT NULL AND c.celular <> '') AS tiene_celular
FROM lds_bronze.bronze_cliente c;
