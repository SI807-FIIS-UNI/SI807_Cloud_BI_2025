CREATE OR REPLACE VIEW gold_db.vw_kpi_atipicos_distrito_mes AS
SELECT
  anio_mes,
  anio,
  mes,
  distrito,
  COUNT(*) AS total_registros,
  COUNT_IF(es_atipico = 1) AS total_atipicos,
  COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
FROM gold_db.vw_facturacion_atipica_detalle
GROUP BY anio_mes, anio, mes, distrito;
