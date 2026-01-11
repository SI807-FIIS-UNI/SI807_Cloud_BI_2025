-- CARGA DE DATA DESDE BUCKETS
--cli_cambios
LOAD DATA INTO `project-sin-477115.refined_data.NOMBRE_TABLA`
FROM FILES(
  format = 'PARQUET',
  uris = ['URI_DEL_GCS']
);
-- registro_comunicaciones_new_v2
LOAD DATA INTO `project-sin-477115.refined_data.registro_comunicaciones_trusted`
FROM FILES(
  format = 'PARQUET',
  uris = ['gs://project-sin-477115-trusted/ingesta/2025-11-30/clean/registro_comunicaciones_new_v2/*']
);

-- segmentos_v2
LOAD DATA INTO `project-sin-477115.refined_data.segmentos_trusted`
FROM FILES(
  format = 'PARQUET',
  uris = ['gs://project-sin-477115-trusted/ingesta/2025-11-30/clean/segmentos_v2/*']
);

-- tiendas_ranking_propio_updated
LOAD DATA INTO `project-sin-477115.refined_data.tiendas_ranking_trusted`
FROM FILES(
  format = 'PARQUET',
  uris = ['gs://project-sin-477115-trusted/ingesta/2025-11-30/clean/tiendas_ranking_propio_updated/*']
);

-- tlv_ranking_propio_updated
LOAD DATA INTO `project-sin-477115.refined_data.tlv_ranking_trusted`
FROM FILES(
  format = 'PARQUET',
  uris = ['gs://project-sin-477115-trusted/ingesta/2025-11-30/clean/tlv_ranking_propio_updated/*']
);

-- virtual_ranking_propio_updated
LOAD DATA INTO `project-sin-477115.refined_data.virtual_ranking_trusted`
FROM FILES(
  format = 'PARQUET',
  uris = ['gs://project-sin-477115-trusted/ingesta/2025-11-30/clean/virtual_ranking_propio_updated/*']
);

----------------------------------------------------------------------------------------------
--CAMBIO DE NOMBRE
-- cli_cambios_trusted -> cli_cambios
ALTER TABLE `project-sin-477115.refined_data.cli_cambios_trusted`
RENAME TO cli_cambios;

-- registro_comunicaciones_trusted -> registro_comunicaciones
ALTER TABLE `project-sin-477115.refined_data.registro_comunicaciones_trusted`
RENAME TO registro_comunicaciones;

-- segmentos_trusted -> segmentos
ALTER TABLE `project-sin-477115.refined_data.segmentos_trusted`
RENAME TO segmentos;

-- tiendas_ranking_trusted -> tiendas_ranking
ALTER TABLE `project-sin-477115.refined_data.tiendas_ranking_trusted`
RENAME TO tiendas_ranking;

-- tlv_ranking_trusted -> tlv_ranking
ALTER TABLE `project-sin-477115.refined_data.tlv_ranking_trusted`
RENAME TO tlv_ranking;

-- virtual_ranking_trusted -> virtual_ranking
ALTER TABLE `project-sin-477115.refined_data.virtual_ranking_trusted`
RENAME TO virtual_ranking;

--------------------------------------------------------------------------------------------------------
--ALGUNAS QUERYS
--Performance segun el tipo de cambio
SELECT
  TIPO,
  COUNT(*) AS num_operaciones,
  SUM(VOL_USD) AS volumen_total_usd,
  AVG(VOL_USD) AS volumen_promedio_usd,
  SUM(Utilidad) AS utilidad_total,
  AVG(Utilidad) AS utilidad_promedio
FROM `project-sin-477115.refined_data.cli_cambios`
GROUP BY TIPO
ORDER BY volumen_total_usd DESC;

--Performance del Volumen de dolares segun el día
WITH ventas_diarias AS (
  SELECT
    DATE(fecha) AS fecha_dia,
    SUM(VOL_USD) AS volumen_total_usd
  FROM `project-sin-477115.refined_data.cli_cambios`
  GROUP BY fecha_dia
)

SELECT
  fecha_dia,
  volumen_total_usd,
  AVG(volumen_total_usd) OVER(
    ORDER BY fecha_dia
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS promedio_7_dias
FROM ventas_diarias
ORDER BY fecha_dia;

-- Performance segun el segmento
WITH cli_con_segmento AS (
  SELECT
    c.fecha,
    c.RUC,
    c.`codigo unico` AS codigo_unico,
    c.Nombre,
    c.TIPO,
    c.VOL_USD,
    c.Utilidad,
    s.`SEGMENTO FX` AS segmento_fx      -- <--- aquí usamos el nombre real
  FROM `project-sin-477115.refined_data.cli_cambios`   AS c
  LEFT JOIN `project-sin-477115.refined_data.segmentos` AS s   -- cámbialo si tu tabla se llama distinto
    ON c.RUC = s.RUC
)

SELECT
  segmento_fx,
  COUNT(*) AS num_operaciones,
  COUNT(DISTINCT RUC) AS clientes_unicos,
  SUM(VOL_USD) AS volumen_total_usd,
  AVG(VOL_USD) AS ticket_promedio_usd,
  SUM(Utilidad) AS utilidad_total,
  AVG(Utilidad) AS utilidad_promedio
FROM cli_con_segmento
GROUP BY segmento_fx
ORDER BY volumen_total_usd DESC;
