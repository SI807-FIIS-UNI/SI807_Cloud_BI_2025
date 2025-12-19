CREATE TABLE lds_silver.silver_tarifa
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/silver/tarifa/'
) AS
SELECT
    t.id_tarifa,
    UPPER(CAST(t.codigo_tarifa AS VARCHAR))   AS codigo_tarifa,
    t.cod_tarifa,
    t.descripcion,
    UPPER(CAST(t.nivel_tension AS VARCHAR))   AS nivel_tension,
    t.segmento_objetivo,
    UPPER(CAST(t.tipo_cliente AS VARCHAR))    AS tipo_cliente,
    t.cargo_fijo,
    t.cargo_energia,
    t.cargo_hp,
    t.cargo_fp,
    -- incluye_demanda la dejamos tal cual (probablemente boolean)
    t.incluye_demanda,
    UPPER(CAST(t.estado_tarifa AS VARCHAR))   AS estado_tarifa,
    CAST(t.fecha_inicio_vigencia AS DATE)     AS fecha_inicio_vigencia
FROM lds_bronze.bronze_tarifa t;

