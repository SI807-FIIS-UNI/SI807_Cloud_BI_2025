CREATE TABLE lds_silver.silver_consolidado_mensual
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/silver/consolidado_mensual/'
) AS
SELECT
    c.id_suministro,
    c.id_medidor,
    c.anio_mes,
    SUBSTRING(c.anio_mes, 1, 4)                 AS anio,
    SUBSTRING(c.anio_mes, 6, 2)                 AS mes,
    c.energia_valle,
    c.energia_pico,
    c.energia_media,
    c.energia_total,
    c.monto_facturado,
    -- Flags de calidad
    (c.energia_total IS NULL)                   AS es_nulo_energia,
    (c.monto_facturado IS NULL)                 AS es_nulo_monto,
    (c.energia_total IS NOT NULL AND c.energia_total < 0) AS es_energia_negativa,
    (c.monto_facturado IS NOT NULL AND c.monto_facturado < 0) AS es_monto_negativo,
    (c.energia_total IS NOT NULL AND c.energia_total = 0) AS es_energia_cero
FROM lds_bronze.bronze_consolidado c;
