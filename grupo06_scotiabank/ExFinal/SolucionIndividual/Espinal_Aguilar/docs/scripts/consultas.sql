-- =====================================================
-- VALIDACIÓN GENERAL
-- =====================================================

-- 1. Vista general de la tabla de hechos
SELECT *
FROM `final-espinal-aguilar.oro.fact_vuelos`
LIMIT 1000;


-- =====================================================
-- 2. Validación de conteo de registros
-- =====================================================
SELECT 
  COUNT(*) AS total_registros
FROM `final-espinal-aguilar.oro.fact_vuelos`;


-- =====================================================
-- 3. Validación de valores nulos
-- =====================================================
SELECT
  SUM(CASE WHEN id_tiempo IS NULL THEN 1 ELSE 0 END) AS nulos_id_tiempo,
  SUM(CASE WHEN id_aerolinea IS NULL THEN 1 ELSE 0 END) AS nulos_id_aerolinea,
  SUM(CASE WHEN id_origen IS NULL THEN 1 ELSE 0 END) AS nulos_id_origen,
  SUM(CASE WHEN id_destino IS NULL THEN 1 ELSE 0 END) AS nulos_id_destino,
  SUM(CASE WHEN id_causa IS NULL THEN 1 ELSE 0 END) AS nulos_id_causa
FROM `final-espinal-aguilar.oro.fact_vuelos`;


-- =====================================================
-- 4. Validación de métricas negativas
-- =====================================================
SELECT
  COUNT(*) AS retrasos_negativos
FROM `final-espinal-aguilar.oro.fact_vuelos`
WHERE arr_delay < 0
   OR dep_delay < 0;


-- =====================================================
-- 5. Validación de retraso total
-- =====================================================
SELECT
  arr_delay,
  dep_delay,
  delay_by_cause,
  (arr_delay + dep_delay) AS retraso_calculado
FROM `final-espinal-aguilar.oro.fact_vuelos`
WHERE delay_by_cause != (arr_delay + dep_delay)
LIMIT 100;


-- =====================================================
-- 6. Validación - DIM_TIEMPO
-- =====================================================
SELECT COUNT(*) AS sin_match_tiempo
FROM `final-espinal-aguilar.oro.fact_vuelos` f
LEFT JOIN `final-espinal-aguilar.oro.dim_tiempo` t
  ON f.id_tiempo = t.id_tiempo
WHERE t.id_tiempo IS NULL;


-- =====================================================
-- 7. Validación - DIM_AEROLINEA
-- =====================================================
SELECT COUNT(*) AS sin_match_aerolinea
FROM `final-espinal-aguilar.oro.fact_vuelos` f
LEFT JOIN `final-espinal-aguilar.oro.dim_aerolinea` a
  ON f.id_aerolinea = a.id_aerolinea
WHERE a.id_aerolinea IS NULL;


-- =====================================================
-- 8. Validación - DIM_ORIGEN
-- =====================================================
SELECT COUNT(*) AS sin_match_origen
FROM `final-espinal-aguilar.oro.fact_vuelos` f
LEFT JOIN `final-espinal-aguilar.oro.dim_origen` o
  ON f.id_origen = o.id_origen
WHERE o.id_origen IS NULL;


-- =====================================================
-- 9. Validación - DIM_DESTINO
-- =====================================================
SELECT COUNT(*) AS sin_match_destino
FROM `final-espinal-aguilar.oro.fact_vuelos` f
LEFT JOIN `final-espinal-aguilar.oro.dim_destino` d
  ON f.id_destino = d.id_destino
WHERE d.id_destino IS NULL;


-- =====================================================
-- 10. Validación - DIM_CAUSA
-- =====================================================
SELECT COUNT(*) AS sin_match_causa
FROM `final-espinal-aguilar.oro.fact_vuelos` f
LEFT JOIN `final-espinal-aguilar.oro.dim_causa` c
  ON f.id_causa = c.id_causa
WHERE c.id_causa IS NULL;


-- =====================================================
-- 11. Distribución de retrasos por causa
-- =====================================================
SELECT
  c.causa_retraso,
  COUNT(*) AS total_vuelos,
  SUM(f.delay_by_cause) AS minutos_retraso
FROM `final-espinal-aguilar.oro.fact_vuelos` f
JOIN `final-espinal-aguilar.oro.dim_causa` c
  ON f.id_causa = c.id_causa
GROUP BY c.causa_retraso
ORDER BY minutos_retraso DESC;


-- =====================================================
-- 12. Muestreo
-- =====================================================
SELECT
  t.fecha,
  a.nombre_aerolinea,
  o.codigo_aeropuerto AS origen,
  d.codigo_aeropuerto AS destino,
  f.dep_delay,
  f.arr_delay,
  f.delay_by_cause
FROM `final-espinal-aguilar.oro.fact_vuelos` f
JOIN `final-espinal-aguilar.oro.dim_tiempo` t
  ON f.id_tiempo = t.id_tiempo
JOIN `final-espinal-aguilar.oro.dim_aerolinea` a
  ON f.id_aerolinea = a.id_aerolinea
JOIN `final-espinal-aguilar.oro.dim_origen` o
  ON f.id_origen = o.id_origen
JOIN `final-espinal-aguilar.oro.dim_destino` d
  ON f.id_destino = d.id_destino
LIMIT 500;
