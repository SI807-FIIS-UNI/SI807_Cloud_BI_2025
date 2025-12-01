-- ============================
-- 03 - KPIs Y MÉTRICAS
-- ============================

-- KPI: Fallecidos por año + porcentaje sobre el total
SELECT
  t.anio,
  COUNT(*) AS total_personas,
  COUNTIF(p.gravedad = 'FALLECIDO') AS fallecidos,
  ROUND(
    SAFE_DIVIDE(
      COUNTIF(p.gravedad = 'FALLECIDO'),
      COUNT(*)
    ) * 100, 2
  ) AS tasa_fallecidos_pct
FROM `sutran.hechos_siniestros` h
JOIN `sutran.dim_tiempo`  t ON h.id_tiempo  = t.id_tiempo
JOIN `sutran.dim_persona` p ON h.id_persona = p.id_persona
GROUP BY t.anio
ORDER BY t.anio;

-- KPI: Siniestros por tipo de persona y día de la semana
SELECT
  t.dia_semana,
  p.tipo_persona,
  COUNT(*) AS total
FROM `sutran.hechos_siniestros` h
JOIN `sutran.dim_tiempo`  t ON h.id_tiempo = t.id_tiempo
JOIN `sutran.dim_persona` p ON h.id_persona = p.id_persona
GROUP BY t.dia_semana, p.tipo_persona
ORDER BY t.dia_semana, total DESC;

-- KPI: Fines de semana vs días de semana
SELECT
  t.es_fin_de_semana,
  COUNT(*) AS total_personas,
  COUNTIF(p.gravedad = 'FALLECIDO') AS fallecidos,
  ROUND(
    SAFE_DIVIDE(COUNTIF(p.gravedad = 'FALLECIDO'), COUNT(*)) * 100, 2
  ) AS tasa_fallecidos_pct
FROM `sutran.hechos_siniestros` h
JOIN `sutran.dim_tiempo` t ON h.id_tiempo = t.id_tiempo
JOIN `sutran.dim_persona` p ON h.id_persona = p.id_persona
GROUP BY t.es_fin_de_semana;
