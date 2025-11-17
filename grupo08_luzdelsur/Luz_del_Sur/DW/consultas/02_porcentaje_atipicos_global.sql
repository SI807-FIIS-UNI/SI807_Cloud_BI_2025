SELECT
  COUNT_IF(es_atipico = 1) * 100.0 / COUNT(*) AS porcentaje_atipicos
FROM gold_db.gold_facturacion_teorica_mes;
