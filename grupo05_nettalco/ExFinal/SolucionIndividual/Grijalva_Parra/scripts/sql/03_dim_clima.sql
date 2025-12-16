-- 03. DIM_CLIMA: Distribución por clima
SELECT
  Source,
  COUNT(*) AS registros
FROM `us-accidents-481401.us_accidents_dw.dim_clima`
GROUP BY Source
ORDER BY registros DESC;
