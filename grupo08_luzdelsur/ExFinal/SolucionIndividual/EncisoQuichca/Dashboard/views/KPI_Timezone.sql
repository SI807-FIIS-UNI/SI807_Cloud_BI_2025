CREATE OR REPLACE VIEW vw_dataexfinal_accidents_by_timezone AS
SELECT
  timezone,
  accident_cnt
FROM kpi_accidents_by_timezone;
