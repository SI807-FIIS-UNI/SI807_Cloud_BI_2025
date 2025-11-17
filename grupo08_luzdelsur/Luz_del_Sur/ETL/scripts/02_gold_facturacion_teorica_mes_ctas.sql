CREATE DATABASE IF NOT EXISTS gold_db;

DROP TABLE IF EXISTS gold_db.gold_facturacion_teorica_mes;

CREATE TABLE gold_db.gold_facturacion_teorica_mes
WITH (
  external_location = 's3://lds-s3-bucket-demo/gold/facturacion_teorica_mes/',
  format = 'PARQUET',
  write_compression = 'SNAPPY'
) AS
WITH base AS (
  SELECT
    cm.id_suministro,
    cm.id_medidor,
    cm.anio_mes,
    cm.energia_total_kwh,
    cm.demanda_max_kw,
    cm.n_registros,
    cm.n_registros_error,
    cm.pct_registros_error,
    s.nivel_tension,
    s.distrito,
    c.tipo_cliente,
    atf.cod_tarifa,
    t.cargo_energia,
    t.cargo_fijo,
    (cm.energia_total_kwh * t.cargo_energia) + t.cargo_fijo AS facturacion_teorica
  FROM silver_db.silver_consumo_mensual cm
  JOIN bronze_db.bronze_suministro s
    ON cm.id_suministro = s.id_suministro
  JOIN bronze_db.bronze_cliente c
    ON s.id_cliente = c.id_cliente
  JOIN bronze_db.bronze_asignacion_tarifa atf
    ON atf.id_suministro = s.id_suministro
   AND atf.estado_asignacion = 'ACTIVO'
  JOIN bronze_db.bronze_tarifa t
    ON t.cod_tarifa = atf.cod_tarifa
),
seg AS (
  SELECT
    *,
    COUNT(*) OVER (
      PARTITION BY tipo_cliente, nivel_tension, anio_mes
    ) AS n_segmento,
    approx_percentile(facturacion_teorica, 0.25) OVER (
      PARTITION BY tipo_cliente, nivel_tension, anio_mes
    ) AS q1,
    approx_percentile(facturacion_teorica, 0.75) OVER (
      PARTITION BY tipo_cliente, nivel_tension, anio_mes
    ) AS q3
  FROM base
),
bounds AS (
  SELECT
    *,
    (q3 - q1) AS iqr,
    q3 + 1.5 * (q3 - q1) AS umbral_superior
  FROM seg
)
SELECT
  *,
  CASE
    WHEN n_segmento >= 30
     AND facturacion_teorica > umbral_superior
    THEN 1 ELSE 0
  END AS es_atipico
FROM bounds;
