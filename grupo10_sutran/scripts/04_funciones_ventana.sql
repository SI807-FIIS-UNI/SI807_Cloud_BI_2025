-- ============================
-- 04 - FUNCIONES VENTANA (LAG, RANK, OVER, PARTITION)
-- ============================

-- RANK por tipos de vía según fallecidos
SELECT
  tv.tipo_de_via_normalizado,
  COUNT(*) AS total_personas,
  COUNTIF(p.gravedad = 'FALLECIDO') AS total_fallecidos,
  RANK() OVER (ORDER BY COUNTIF(p.gravedad = 'FALLECIDO') DESC) AS ranking
FROM `sutran.hechos_siniestros` h
JOIN `sutran.dim_tipo_via` tv ON h.id_tipo_via = tv.id_tipo_via
JOIN `sutran.dim_persona` p ON h.id_persona = p.id_persona
GROUP BY tv.tipo_de_via_normalizado
ORDER BY total_fallecidos DESC;

-- LAG: evolución mensual de siniestros
WITH mensual AS (
  SELECT
    t.anio,
    t.mes,
    COUNT(*) AS total_siniestros
  FROM `sutran.hechos_siniestros` h
  JOIN `sutran.dim_tiempo` t ON h.id_tiempo = t.id_tiempo
  GROUP BY t.anio, t.mes
)
SELECT
  anio,
  mes,
  total_siniestros,
  LAG(total_siniestros) OVER (ORDER BY anio, mes) AS total_mes_anterior,
  total_siniestros - LAG(total_siniestros) OVER (ORDER BY anio, mes) AS variacion_abs,
  ROUND(
    SAFE_DIVIDE(
      total_siniestros - LAG(total_siniestros) OVER (ORDER BY anio, mes),
      LAG(total_siniestros) OVER (ORDER BY anio, mes)
    ) * 100, 2
  ) AS variacion_pct
FROM mensual
ORDER BY anio, mes;

-- Distribución porcentual por edad usando ventanas
SELECT
  p.edad,
  COUNT(*) AS total,
  SUM(COUNT(*)) OVER () AS total_global,
  ROUND(
    SAFE_DIVIDE(COUNT(*), SUM(COUNT(*)) OVER ()) * 100, 2
  ) AS porcentaje
FROM `sutran.hechos_siniestros` h
JOIN `sutran.dim_persona` p ON h.id_persona = p.id_persona
GROUP BY p.edad
ORDER BY p.edad;
