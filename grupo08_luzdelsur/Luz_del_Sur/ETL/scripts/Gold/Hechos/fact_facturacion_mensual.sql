CREATE TABLE lds_gold.fact_facturacion_mensual
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/fact_facturacion_mensual/'
) AS
SELECT
    c.id_suministro,
    s.id_cliente,
    s.id_ubicacion,
    c.id_medidor,
    a.id_tarifa,
    c.anio_mes,
    CAST(c.anio AS INTEGER) AS anio,
    CAST(c.mes AS INTEGER)  AS mes,
    c.energia_valle,
    c.energia_pico,
    c.energia_media,
    c.energia_total,
    c.monto_facturado,
    -- flags de calidad
    c.es_nulo_energia,
    c.es_nulo_monto,
    c.es_energia_negativa,
    c.es_monto_negativo,
    c.es_energia_cero
FROM lds_silver.silver_consolidado_mensual c
LEFT JOIN lds_silver.silver_suministro s
    ON c.id_suministro = s.id_suministro
LEFT JOIN lds_silver.silver_asign_tarifa a
    ON c.id_suministro = a.id_suministro;
