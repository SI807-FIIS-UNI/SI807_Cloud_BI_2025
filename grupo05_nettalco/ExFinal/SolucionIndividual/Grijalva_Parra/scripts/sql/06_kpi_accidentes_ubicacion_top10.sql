-- 06. KPI_ACCIDENTES_UBICACION (Top 10 hotspots)
SELECT
  lat_bucket,
  lng_bucket,
  total_accidentes
FROM `us-accidents-481401.us_accidents_dw.kpi_accidentes_ubicacion`
ORDER BY total_accidentes DESC
LIMIT 10;
