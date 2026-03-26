-- ============================
-- 05 - RANKING AVANZADO
-- ============================

-- Ranking por tipo de persona según fallecidos
SELECT
  p.tipo_persona,
  COUNT(*) AS total_personas,
  COUNTIF(p.gravedad = 'FALLECIDO') AS total_fallecidos,
  RANK() OVER (ORDER BY COUNTIF(p.gravedad = 'FALLECIDO') DESC) AS ranking
FROM `sutran.hechos_siniestros` h
JOIN `sutran.dim_persona` p ON h.id_persona = p.id_persona
GROUP BY p.tipo_persona
ORDER BY total_fallecidos DESC;
