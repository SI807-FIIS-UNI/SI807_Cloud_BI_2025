-- 09. QUERY ESTRELLA (JOIN COMPLETO PARA ANALISIS)
SELECT
  t.hora,
  u.lat_bucket,
  u.lng_bucket,
  AVG(f.Severity) AS severidad_promedio,
  COUNT(*) AS accidentes
FROM `us-accidents-481401.us_accidents_dw.fact_accidentes` f
JOIN `us-accidents-481401.us_accidents_dw.dim_tiempo` t
  ON f.Start_Time_ts = t.fecha
JOIN `us-accidents-481401.us_accidents_dw.dim_ubicacion` u
  ON f.lat_bucket = u.lat_bucket
 AND f.lng_bucket = u.lng_bucket
GROUP BY t.hora, u.lat_bucket, u.lng_bucket
ORDER BY accidentes DESC
LIMIT 10;
