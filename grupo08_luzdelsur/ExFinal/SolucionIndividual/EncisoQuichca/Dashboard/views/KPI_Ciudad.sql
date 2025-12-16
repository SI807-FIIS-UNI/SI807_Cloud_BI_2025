CREATE OR REPLACE VIEW vw_dataexfinal_accidents_by_city AS
SELECT
  state,
  city,
  accident_cnt,
  avg_severity
FROM kpi_accidents_by_city;
