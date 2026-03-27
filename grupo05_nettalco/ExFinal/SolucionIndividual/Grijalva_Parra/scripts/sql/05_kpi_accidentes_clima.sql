-- 05. KPI_ACCIDENTES_CLIMA
SELECT
  Source,
  total_accidentes
FROM `us-accidents-481401.us_accidents_dw.kpi_accidentes_clima`
ORDER BY total_accidentes DESC;
