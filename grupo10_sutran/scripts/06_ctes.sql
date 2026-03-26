-- ============================
-- 06 - CTEs Y ANALÍTICA AVANZADA
-- ============================

WITH base AS (
  SELECT
    t.anio,
    tv.tipo_de_via_normalizado,
    p.tipo_persona,
    p.gravedad
  FROM `sutran.hechos_siniestros` h
  JOIN `sutran.dim_tiempo`   t  ON h.id_tiempo = t.id_tiempo
  JOIN `sutran.dim_tipo_via` tv ON h.id_tipo_via = tv.id_tipo_via
  JOIN `sutran.dim_persona`  p  ON h.id_persona  = p.id_persona
)
SELECT
  anio,
  tipo_de_via_normalizado,
  tipo_persona,
  COUNT(*) AS total_personas,
  COUNTIF(gravedad = 'FALLECIDO') AS total_fallecidos
FROM base
GROUP BY anio, tipo_de_via_normalizado, tipo_persona
ORDER BY anio, total_fallecidos DESC;
