CREATE TABLE lds_gold.dim_tarifa
WITH (
  format = 'PARQUET',
  external_location = 's3://lds-s3-bucket-final/gold/dim_tarifa/'
) AS
SELECT
    t.id_tarifa,
    t.codigo_tarifa,
    t.cod_tarifa,
    t.descripcion,
    t.nivel_tension,
    t.segmento_objetivo,
    t.tipo_cliente,
    t.cargo_fijo,
    t.cargo_energia,
    t.cargo_hp,
    t.cargo_fp,
    t.incluye_demanda,        -- probablemente boolean
    t.estado_tarifa,
    t.fecha_inicio_vigencia
FROM lds_silver.silver_tarifa t;
