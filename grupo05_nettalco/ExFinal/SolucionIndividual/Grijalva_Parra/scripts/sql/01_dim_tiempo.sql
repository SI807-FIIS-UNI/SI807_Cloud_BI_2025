-- 01. DIM_TIEMPO: Cobertura temporal
SELECT
  MIN(fecha) AS fecha_min,
  MAX(fecha) AS fecha_max,
  COUNT(DISTINCT hora) AS horas_distintas
FROM `us-accidents-481401.us_accidents_dw.dim_tiempo`;
