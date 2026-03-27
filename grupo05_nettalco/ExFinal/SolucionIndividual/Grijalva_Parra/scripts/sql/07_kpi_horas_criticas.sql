-- 07. KPI_HORAS_CRITICAS
SELECT
  hora,
  total_accidentes
FROM `us-accidents-481401.us_accidents_dw.kpi_horas_criticas`
ORDER BY total_accidentes DESC;
