-- 04. FACT_ACCIDENTES: Métricas generales
SELECT
  MIN(Severity) AS severidad_min,
  MAX(Severity) AS severidad_max,
  AVG(Duration_minutes) AS duracion_promedio,
  COUNT(*) AS total_accidentes
FROM `us-accidents-481401.us_accidents_dw.fact_accidentes`;
