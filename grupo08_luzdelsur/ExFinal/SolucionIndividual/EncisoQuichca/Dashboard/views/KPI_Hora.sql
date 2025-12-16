CREATE OR REPLACE VIEW vw_dataexfinal_accidents_by_hour AS
SELECT
  hour,
  accident_cnt
FROM kpi_accidents_by_hour;
