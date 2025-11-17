CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_mes AS
SELECT
  anio_mes,
  SUBSTR(anio_mes, 1, 4) AS anio,
  SUBSTR(anio_mes, 6, 2) AS mes,
  COUNT(*) AS total_registros,
  COUNT_IF(es_atipico = 1) AS total_atipicos,
  COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
FROM gold_db.gold_facturacion_teorica_mes
GROUP BY anio_mes;
