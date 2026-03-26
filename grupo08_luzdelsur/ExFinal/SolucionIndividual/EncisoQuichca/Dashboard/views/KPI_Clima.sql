CREATE OR REPLACE VIEW vw_dataexfinal_accidents_by_weather AS
SELECT
  weather_condition,
  accident_cnt,
  avg_severity
FROM kpi_accidents_by_weather;
